from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .models import Member
from .forms import MemberCreateForm


class MemberLoginView(LoginView):
    """View for logging in users"""
    template_name = 'registration/login.html'
    next = '/'


class MemberLogoutView(LogoutView):
    """View for logging out users"""
    next_page = '/'


class MemberListView(ListView):
    """View for listing members"""
    model = Member
    template_name = 'members/list.html'


class MemberCreateView(CreateView):
    """View for creating member"""
    model = Member
    form_class = MemberCreateForm
    template_name = 'members/register.html'
    success_url = reverse_lazy('members:list')


class MemberDetailView(DetailView):
    """View for displaying member detail"""
    model = Member
    template_name = 'members/profile.html'
    context_object_name = 'member'
    pk_url_kwarg = 'member_id'
