from django import forms

from .models import Member


class MemberCreateForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Member
        fields = ['name', 'email', 'password']

        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        """Check the two password inputs are equal"""
        cleaned_data = super().clean()

        if cleaned_data.get("password") != cleaned_data.get("password2"):
            error = forms.ValidationError("The two passwords must match")
            self.add_error('password', error)
            self.add_error('password2', error)

        return cleaned_data
