from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Project
from .forms import ProjectCreateForm


class ProjectListView(ListView):
    """View for listing projects"""

    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    """View for displaying project details"""

    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'
    pk_url_kwarg = 'pk'


class ProjectCreateView(CreateView):
    """View for creating new projects"""

    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/create.html'

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})
