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
                project = self.model.objects.get(pk=self.kwargs['pk'])
                return project in self.request.user.projects.all()

            if self.model == Bug:
                current_bug = Bug.objects.get(id=self.kwargs['pk'])
                return current_bug.project in self.request.user.projects.all()

        print('IsInProjectMixin should be used only on models view of projects\
            and bugs!')
        return False


class IsSupervisorMixin(UserPassesTestMixin):
    """Mixin that only allows to view if user is a supervisor of the project"""
    login_url = reverse_lazy('members:login')

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        if self.model:
            if self.model == Project:
                supervised_projs = self.request.user.supervised_projects.all()
                current_project = self.model.get(pk=self.kwargs['pk'])
                return current_project in supervised_projs

            if self.model == Bug:
                current_bug = Bug.objects.get(id=self.kwargs['pk'])
                supervised_projs = self.request.user.supervised_projects.all()
                return current_bug.project in supervised_projs

        print('IsSupervisorMixin should be used only on models views of \
            projects and bugs!')
        return False


class IsSupervisorOrAssignedMixin(UserPassesTestMixin):
    """Mixin that only allows to view if user is a supervisor of the project"""
    login_url = reverse_lazy('members:login')

    def test_func(self):
        if self.model != Bug:
            print('IsSupervisorOrAssignedMixin should be used only on model \
                views of bugs!')
            return False

        if self.request.user.is_superuser:
            return True

        bug = Bug.objects.get(id=self.kwargs['pk'])
        supervised_projs = self.request.user.supervised_projects.all()

        return bug.project in supervised_projs or \
            self.request.user in bug.assigned_members.all()
