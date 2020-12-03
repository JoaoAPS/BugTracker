from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class IsSuperuserMixin(UserPassesTestMixin):
    """Mixin that makes the view superuser only"""
    login_url = reverse_lazy('members:login')
    permission_denied_message = 'You must an admin to register a new member!'

    def test_func(self):
        """Test if the user is a superuser"""
        return self.request.user.is_superuser


class IsSuperuserOrCurrentUserMixin(UserPassesTestMixin):
    """Mixin that makes the view superuser only"""
    login_url = reverse_lazy('members:login')

    def test_func(self):
        """Test if the user is a superuser"""
        return (
            self.request.user.is_superuser or
            self.request.user.id == self.kwargs['pk']
        )
