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

    def __init__(self, queryset, *args, **kwargs):
        super(BugUpdateForm, self).__init__(*args, **kwargs)
        self.fields['assigned_members'].queryset = queryset

    class Meta:
        model = Bug
        exclude = [
            '_status',
            'creationDate',
            'closingDate',
            'creator',
            'project',
        ]


class BugCreatorUpdateForm(forms.ModelForm):
    """Form for updating a Bug object's title and description"""

    class Meta:
        model = Bug
        fields = ['title', 'description']
