from django.urls import path

from . import views


app_name = 'bugs'

urlpatterns = [
    path('', views.BugListView.as_view(), name='list'),
    path('<int:pk>', views.BugDetailView.as_view(), name='detail'),
    path('create', views.BugCreateView.as_view(), name='create'),
    path('<int:pk>/edit', views.BugUpdateView.as_view(), name='update'),
    path(
        '<int:pk>/assign_member',
        views.BugAssignMemberView.as_view(),
        name='assign_member'
    ),
    path(
        '<int:pk>/change_status',
        views.BugChangeStatusView.as_view(),
        name='change_status'
    ),
]
