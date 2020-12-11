from django.urls import path

from . import views


app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('<int:pk>', views.ProjectDetailView.as_view(), name='detail'),
    path('create', views.ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/edit', views.ProjectUpdateView.as_view(), name='update'),
    path(
        '<int:pk>/add_member',
        views.ProjectAddMemberView.as_view(),
        name='add_member'
    ),
    path(
        '<int:pk>/add_supervisor',
        views.ProjectAddSupervisorView.as_view(),
        name='add_supervisor'
    ),
    path(
        '<int:pk>/change_status',
        views.ProjectChangeStatusView.as_view(),
        name='change_status'
    ),
]
