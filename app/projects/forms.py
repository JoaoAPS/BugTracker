from django import forms

from .models import Project


class ProjectCreateForm(forms.ModelForm):
    def __init__(self, member_options, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields['members'].queryset = member_options

    class Meta:
        model = Project
        exclude = ['_status', 'creationDate', 'closingDate', 'supervisors']


class ProjectUpdateForm(forms.ModelForm):
    def __init__(self, supervisor_options, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)
        self.fields['supervisors'].queryset = supervisor_options

    class Meta:
        model = Project
        exclude = ['_status', 'creationDate', 'closingDate']
