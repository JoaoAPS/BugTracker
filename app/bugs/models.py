from django.db import models

from members.models import Member
from projects.models import Project


class Bug(models.Model):
    """A bug in a project to be fixed"""
    POSSIBLE_STATUS = ['WAITING', 'BEING WORKED', 'FIXED', 'CLOSED']
    ACTIVE_STATUS = ['WAITING', 'BEING WORKED']
    STATUS_CLASSES = {
        'WAITING': 'warning',
        'BEING WORKED': 'primary',
        'FIXED': 'success',
        'CLOSED': 'danger'
    }

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    _status = models.CharField(max_length=15, default='WAITING')
    creationDate = models.DateField(auto_now_add=True)
    closingDate = models.DateField(null=True, blank=True, default=None)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='bugs'
    )
    creator = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='created_bugs'
    )
    assigned_members = models.ManyToManyField(
        Member, related_name='assigned_bugs'
    )

    @property
    def status(self):
        return self._status

    def set_status(self, status):
        """Set the status of the bug checking for valid status"""
        if status not in self.POSSIBLE_STATUS:
            possibleVals = str(self.POSSIBLE_STATUS).strip('[]')
            raise ValueError(
                'Bug status must be one of the following: ' + possibleVals
            )

        self._status = status

    @classmethod
    def get_active(cls):
        """Return a queryset with the active bugs"""
        return cls.objects.filter(_status__in=cls.ACTIVE_STATUS)

    def __str__(self):
        """Return the string representation of the bug object"""
        return self.title

    __repr__ = __str__
