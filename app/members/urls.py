from django.urls import path

from . import views


app_name = 'members'

urlpatterns = [
    path('', views.MemberListView.as_view(), name='list'),
    path(
        '<int:member_id>',
        views.MemberDetailView.as_view(),
        name='profile'
    ),
    path('login', views.MemberLoginView.as_view(), name='login'),
    path('logout', views.MemberLogoutView.as_view(), name='logout'),
    path('register', views.MemberCreateView.as_view(), name='register'),
]
