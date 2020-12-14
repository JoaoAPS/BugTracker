from django.urls import path

from . import views
from members.views import MemberProfileView


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', MemberProfileView.as_view(), name='member-profile'),
]
