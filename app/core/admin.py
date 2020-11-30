from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from members.models import Member


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
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
