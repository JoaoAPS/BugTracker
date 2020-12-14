from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('members/', include('members.urls')),
    path('projects/', include('projects.urls')),
    path('bugs/', include('bugs.urls')),
]
