from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from members.models import Member
from projects.models import Project
from bugs.models import Bug


class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'email', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('name', 'email')
    ordering = ('name',)


admin.site.register(Member, UserAdmin)
admin.site.register(Project)
admin.site.register(Bug)
