from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bug
from .forms import BugCreationForm
from core.mixins import IsInProjectMixin


class BugListView(LoginRequiredMixin, ListView):
    """View for listing bugs"""
    model = Bug
    template_name = 'bugs/list.html'
    context_object_name = 'bugs'


class BugDetailView(IsInProjectMixin, DetailView):
    """View for display bug detail"""
    model = Bug
    template_name = 'bugs/detail.html'
    context_object_name = 'bug'


class BugCreateView(LoginRequiredMixin, CreateView):
    """View for creating bugs"""
    form_class = BugCreationForm
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
