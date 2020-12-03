from django import forms

from .models import Bug


class BugCreationForm(forms.ModelForm):
    """Form for the creation of a Bug object"""

    class Meta:
        model = Bug
        exclude = ['_status', 'creationDate', 'closingDate', 'creator']
        widgets = {'creator': forms.HiddenInput}
