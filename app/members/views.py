from django.views.generic.list import ListView

from .models import Member


class MemberListView(ListView):
    """View for listing members"""
    model = Member
    template_name = 'members/list.html'
