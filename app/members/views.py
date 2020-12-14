from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Member
from .forms import MemberCreateForm
from core.mixins import IsSuperuserMixin


class MemberLoginView(LoginView):
    """View for logging in users"""
    template_name = 'registration/login.html'


class MemberLogoutView(LoginRequiredMixin, LogoutView):
    """View for logging out users"""
    next_page = '/'
    login_url = reverse_lazy('members:login')


class MemberListView(LoginRequiredMixin, ListView):
    """View for listing members"""
    model = Member
    template_name = 'members/list.html'
    context_object_name = 'members'
    login_url = reverse_lazy('members:login')

    def get_queryset(self):
        """Return the queryset after ordering"""
        return self.model.objects.all().order_by('name')


class MemberCreateView(IsSuperuserMixin, CreateView):
    """View for creating member"""
    model = Member
    form_class = MemberCreateForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('members:list')

    def form_valid(self, form):
        """If the form is valid, add the creator and save the object"""
        self.object = form.save(commit=False)
        self.object.is_staff = self.object.is_superuser
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class MemberDetailView(LoginRequiredMixin, DetailView):
    """View for displaying member detail"""
    model = Member
    template_name = 'members/detail.html'
    context_object_name = 'member'
    login_url = reverse_lazy('members:login')


class MemberProfileView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'members/profile.html'
    context_object_name = 'member'
    login_url = reverse_lazy('members:login')

    def get_object(self):
        """Return the current authenticated member"""
        return self.request.user
