from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project
from .forms import ProjectCreateForm
from core.mixins import IsInProjectMixin, IsSupervisorMixin


class ProjectListView(LoginRequiredMixin, ListView):
    """View for listing projects"""
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    login_url = reverse_lazy('members:login')


class ProjectDetailView(IsInProjectMixin, DetailView):
    """View for displaying project details"""
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        """Add additional data to the context"""
        context = super().get_context_data(**kwargs)

        context['user_bugs'] = self.object.bugs.filter(
            assigned_members__id__contains=self.request.user.id
        )
        context['other_bugs'] = self.object.bugs.exclude(
            assigned_members__id__contains=self.request.user.id
        )

        context['isAdminOrSupervisor'] = (
            self.request.user.is_superuser or
            self.request.user in self.object.supervisors.all()
        )

        context['status_class'] = {
            'ON-GOING': 'text-primary',
            'CLOSED': 'text-danger',
            'FINISHED': 'text-success',
            'PAUSED': 'text-secondary'
        }[self.object.status]

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """View for creating new projects"""
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/create.html'
    login_url = reverse_lazy('members:login')

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(IsSupervisorMixin, UpdateView):
    """View for creating new projects"""
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/update.html'
    login_url = reverse_lazy('members:login')

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})
