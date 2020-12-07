from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Home page view of the application"""
    template_name = 'core/index.html'
