from django.urls import path

from . import views


app_name = 'bugs'

urlpatterns = [
    path('', views.BugListView.as_view(), name='list'),
    path('<int:pk>', views.BugDetailView.as_view(), name='detail'),
    path('create', views.BugCreateView.as_view(), name='create'),
]
