from django import forms

from .models import Bug


class BugCreateForm(forms.ModelForm):
    """Form for the creation of a Bug object"""

    class Meta:
        model = Bug
        exclude = [
            '_status',
            'creationDate',
            'closingDate',
            'creator',
            'assigned_members'
        ]


class BugUpdateForm(forms.ModelForm):
    """Form for updating a Bug object"""

    class Meta:
        model = Bug
        exclude = [
            '_status',
            'creationDate',
            'closingDate',
            'creator',
        ]
