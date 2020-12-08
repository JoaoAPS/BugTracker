from django.contrib import admin
from django.urls import path, include

from core.views import IndexView
from members.views import MemberProfileView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
    path('projects/', include('projects.urls')),
    path('bugs/', include('bugs.urls')),
    path('profile/', MemberProfileView.as_view(), name='member-profile'),
]
