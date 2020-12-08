from django.contrib.auth.views import LoginView


class IndexView(LoginView):
    """Home page view of the application"""
    template_name = 'core/index.html'
    redirect_authenticated_user = True
