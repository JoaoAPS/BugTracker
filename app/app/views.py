from django.http import HttpResponse


def indexView(request):
    """Home page view of the application"""
    return HttpResponse('<h1>Home<h1>')
