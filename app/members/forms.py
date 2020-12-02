from django import forms

from .models import Member


class MemberCreateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'password', 'is_superuser']
        widgets = {
            'password': forms.PasswordInput
        }
