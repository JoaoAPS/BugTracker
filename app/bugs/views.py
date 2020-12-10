from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.http.response import HttpResponseBadRequest
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bug
from .forms import BugCreateForm, BugUpdateForm
from core.mixins import IsInProjectMixin, IsSupervisorMixin
from members.models import Member


class BugListView(LoginRequiredMixin, ListView):
    """View for listing bugs"""
    model = Bug
    template_name = 'bugs/list.html'
    context_object_name = 'bugs'
    login_url = reverse_lazy('members:login')


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

        context['status_class'] = {
            'WAITING': 'text-warning',
            'BEING WORKED': 'text-primary',
            'FIXED': 'text-success'
        }[self.object.status]

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


class BugUpdateView(LoginRequiredMixin, UpdateView):
    """View for creating bugs"""
    model = Bug
    form_class = BugUpdateForm
    template_name = 'bugs/update.html'
    login_url = reverse_lazy('members:login')

    def get_success_url(self):
        """Return the url to the current object detail page"""
        return reverse_lazy('bugs:detail', args=[self.object.id])


class BugAssignMemberView(IsSupervisorMixin, View):
    """Perform assignment of member to bug"""

    def post(self, request, pk):
        bug = get_object_or_404(Bug, pk=pk)

        try:
            member = Member.objects.get(id=request.POST['member_id'])
            if member not in bug.project.members.all():
                return HttpResponseBadRequest()
            bug.assigned_members.add(member)
        except Member.DoesNotExist:
            return HttpResponseBadRequest()

        return redirect('bugs:detail', pk=pk)
