from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import SuspiciousOperation

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bug
from .forms import BugCreateForm, BugUpdateForm
from core.mixins import \
    IsInProjectMixin, \
    IsSupervisorMixin, \
    IsSupervisorOrAssignedMixin
from members.models import Member


class BugListView(LoginRequiredMixin, ListView):
    """View for listing bugs"""
    model = Bug
    template_name = 'bugs/list.html'
    context_object_name = 'bugs'
    login_url = reverse_lazy('members:login')

    def get_queryset(self):
        """Return the list of projects applting filters"""
        queryset = self.model.objects.all() \
            if self.request.GET.get('show_inactive') \
            else self.model.get_active().all()

        return queryset


class BugDetailView(IsInProjectMixin, DetailView):
    """View for display bug detail"""
    model = Bug
    template_name = 'bugs/detail.html'
    context_object_name = 'bug'

    def get_context_data(self, **kwargs):
        """Add additional data to the context"""
        context = super().get_context_data(**kwargs)

        context['isAdminOrSupervisor'] = (
            self.request.user.is_superuser or
            self.request.user in self.object.project.supervisors.all()
        )

        context['status_class'] = 'text-' + self.object.STATUS_CLASSES[
            self.object.status
        ]

        return context


class BugCreateView(LoginRequiredMixin, CreateView):
    """View for creating bugs"""
    model = Bug
    form_class = BugCreateForm
    template_name = 'bugs/create.html'
    login_url = reverse_lazy('members:login')

    def get_success_url(self):
        """Return the url to the current object detail page"""
        return reverse_lazy('bugs:detail', args=[self.object.id])

    def form_valid(self, form):
        """If the form is valid, add the creator and save the object"""
        if not self.request.user.is_authenticated:
            print("Bug creation of unauthenticated user denied!")
            return redirect(self.login_url)
            return

        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())

    def get_initial(self):
        """Set the active project if supplied in GET param"""
        project = self.request.GET.get('project')
        if project:
            return {'project': int(project)}
        return {}


class BugUpdateView(LoginRequiredMixin, UpdateView):
    """View for creating bugs"""
    model = Bug
    form_class = BugUpdateForm
    template_name = 'bugs/update.html'
    login_url = reverse_lazy('members:login')

    def get_success_url(self):
        """Return the url to the current object detail page"""
        return reverse_lazy('bugs:detail', args=[self.object.id])

    def get_form(self, form_class=None):
        """Return a form with the correct queryset"""
        if form_class is None:
            form_class = self.get_form_class()

        if self.object and self.object.project:
            project_members = self.object.project.members.all()
            return form_class(project_members, **self.get_form_kwargs())
        return form_class(None, **self.get_form_kwargs())


class BugAssignMemberView(IsSupervisorMixin, View):
    """Perform assignment of member to bug"""

    def post(self, request, pk):
        bug = get_object_or_404(Bug, pk=pk)

        member_ids = request.POST.getlist('member_ids')
        if not member_ids:
            raise SuspiciousOperation('Member id not sent!')
        member_ids = [int(m_id) for m_id in member_ids]

        try:
            for member_id in member_ids:
                member = Member.objects.get(id=member_id)
                if member not in bug.project.members.all():
                    return SuspiciousOperation(
                        'Member must be part of bug project!'
                    )
                bug.assigned_members.add(member)
        except Member.DoesNotExist:
            return SuspiciousOperation('Invalid member id!')

        return redirect('bugs:detail', pk=pk)


class BugChangeStatusView(IsSupervisorMixin, View):
    """Change the status of the bug"""

    def post(self, request, pk):
        bug = get_object_or_404(Bug, pk=pk)
        status = request.POST.get('status')

        if not status:
            return SuspiciousOperation('New status must be sent in POST')

        try:
            bug.set_status(status)
            bug.save()
        except ValueError:
            return SuspiciousOperation('Invalid status')

        return redirect('bugs:detail', pk=pk)


class BugChangeWorkingStatusView(IsSupervisorOrAssignedMixin, View):
    """Change the status of the bug"""
    model = Bug

    def post(self, request, pk):
        bug = get_object_or_404(Bug, pk=pk)
        starting = request.POST.get('starting')

        if starting is None:
            return SuspiciousOperation(
                'Value of starting must be sent in POST'
            )

        try:
            bug.set_status(
                bug.WORKING_STATUS if int(starting) else bug.WAITING_STATUS
            )
            bug.save()
        except ValueError:
            return SuspiciousOperation('Invalid status')

        return redirect('bugs:detail', pk=pk)
