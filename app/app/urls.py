from django.contrib import admin
from django.urls import path, include

from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
    path('projects/', include('projects.urls')),
    path('bugs/', include('bugs.urls')),
]
