from django.urls import path

from . import views


app_name = 'members'

urlpatterns = [
    path('', views.MemberListView.as_view(), name='list'),
    path('register', views.MemberCreateView.as_view(), name='register'),
    path(
        '<int:member_id>',
        views.MemberDetailView.as_view(),
        name='profile'
    ),
]
