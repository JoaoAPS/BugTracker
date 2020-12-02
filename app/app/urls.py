from django.contrib import admin
from django.urls import path, include

from .views import indexView

urlpatterns = [
    path('', indexView),
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
]
