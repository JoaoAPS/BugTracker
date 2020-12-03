from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from projects.models import Project
from bugs.models import Bug


class IsSuperuserMixin(UserPassesTestMixin):
    """Mixin that only allows to view superusers"""
    login_url = reverse_lazy('members:login')
    permission_denied_message = 'You must an admin to register a new member!'

    def test_func(self):
        return self.request.user.is_superuser


class IsCurrentUserMixin(UserPassesTestMixin):
    """Mixin that only allows to view if superuser or matching logged user"""
    login_url = reverse_lazy('members:login')

    def test_func(self):
        return (
            self.request.user.is_superuser or
            self.request.user.id == self.kwargs['pk']
        )


class IsInProjectMixin(UserPassesTestMixin):
    """Mixin that only allows to view if user is part of the project"""
    login_url = reverse_lazy('members:login')

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        if self.model:
            if self.model == Project:
                return self.kwargs['pk'] in self.request.user.projects.all()

            if self.model == Bug:
                current_bug = Bug.objects.get(id=self.kwargs['pk'])
                return current_bug.project in self.request.user.projects.all()

        print('IsInProjectMixin should be used only on models view of projects\
            and bugs!')
        return False
