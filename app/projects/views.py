from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project
from .forms import ProjectCreateForm, ProjectUpdateForm
from core.mixins import IsInProjectMixin, IsSupervisorMixin


class ProjectListView(LoginRequiredMixin, ListView):
    """View for listing projects"""
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    login_url = reverse_lazy('members:login')

    def get_queryset(self):
        """Return the list of projects applting filters and ordering"""
        queryset = self.model.objects.all() \
            if self.request.GET.get('show_inactive') \
            else self.model.get_active()

        return queryset.order_by('-creationDate')


class ProjectDetailView(IsInProjectMixin, DetailView):
    """View for displaying project details"""
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        """Add additional data to the context"""
        context = super().get_context_data(**kwargs)

        context['user_bugs'] = self.object.active_bugs.filter(
            assigned_members__id__contains=self.request.user.id
        )
        context['other_bugs'] = self.object.active_bugs.exclude(
            assigned_members__id__contains=self.request.user.id
        )

        context['isAdminOrSupervisor'] = (
            self.request.user.is_superuser or
            self.request.user in self.object.supervisors.all()
        )

        context['status_class'] = self.object.STATUS_CLASSES[
            self.object.status
        ]

        context['all_members'] = get_user_model().objects.all()

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """View for creating new projects"""
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/create.html'
    login_url = reverse_lazy('members:login')

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        """Return a form with the correct queryset"""
        if form_class is None:
            form_class = self.get_form_class()

        members_to_add = get_user_model().objects.filter(
            ~Q(id=self.request.user.id)
        )

        return form_class(members_to_add, **self.get_form_kwargs())

    def form_valid(self, form):
        """Creates the project and sets the current user as supervisor"""
        project = form.save()

        project.members.add(self.request.user)
        project.supervisors.add(self.request.user)
        project.save()

        self.object = project

        return redirect(self.get_success_url())


class ProjectUpdateView(IsSupervisorMixin, UpdateView):
    """View for creating new projects"""
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'projects/update.html'
    login_url = reverse_lazy('members:login')

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        """Return a form with the correct queryset"""
        if form_class is None:
            form_class = self.get_form_class()

        if self.object:
            project_members = self.object.members.all()
            return form_class(project_members, **self.get_form_kwargs())

        return form_class(None, **self.get_form_kwargs())


class ProjectAddMemberView(IsSupervisorMixin, View):
    """Add a member to the project"""

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        member_ids = request.POST.getlist('member_ids')
        MemberModel = get_user_model()

        if not member_ids:
            raise SuspiciousOperation('Member ids must be passed!')

        member_ids = [int(m_id) for m_id in member_ids]

        try:
            for member_id in member_ids:
                member = MemberModel.objects.get(id=member_id)
                project.members.add(member)
        except MemberModel.DoesNotExist:
            raise SuspiciousOperation('Invalid member id!')

        return redirect('projects:detail', pk=pk)


class ProjectAddSupervisorView(IsSupervisorMixin, View):
    """Add a supervisor to the project"""

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        supervisor_ids = request.POST.getlist('supervisor_ids')
        MemberModel = get_user_model()

        if not supervisor_ids:
            raise SuspiciousOperation('Member ids must be passed!')

        supervisor_ids = [int(m_id) for m_id in supervisor_ids]

        try:
            for supervisor_id in supervisor_ids:
                member = MemberModel.objects.get(id=supervisor_id)
                if member not in project.members.all():
                    raise SuspiciousOperation(
                        'Member must be in the project to be assigned \
                        supervisor!'
                    )
                project.supervisors.add(member)
        except MemberModel.DoesNotExist:
            raise SuspiciousOperation('Invalid member id!')

        return redirect('projects:detail', pk=pk)


class ProjectChangeStatusView(IsSupervisorMixin, View):
    """Change the status of the project"""

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        status = request.POST.get('status')

        if not status:
            raise SuspiciousOperation('New status must be sent in POST')

        try:
            project.set_status(status)
            project.save()
        except ValueError:
            raise SuspiciousOperation('Invalid status')

        return redirect('projects:detail', pk=pk)
