from django.db import models
from django.contrib.auth import get_user_model

from projects.models import Project


class Bug(models.Model):
    """A bug in a project to be fixed"""
    POSSIBLE_STATUS = ['BEING WORKED', 'WAITING', 'FIXED', 'CLOSED']
    ACTIVE_STATUS = ['WAITING', 'BEING WORKED']
    WORKING_STATUS = 'BEING WORKED'
    WAITING_STATUS = 'WAITING'
    STATUS_CLASSES = {
        'WAITING': 'warning',
        'BEING WORKED': 'primary',
        'FIXED': 'success',
        'CLOSED': 'danger'
    }

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    _status = models.CharField(max_length=15, default='WAITING')
    creationDate = models.DateTimeField(auto_now_add=True)
    closingDate = models.DateTimeField(null=True, blank=True, default=None)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='bugs'
    )
    creator = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='created_bugs'
    )
    assigned_members = models.ManyToManyField(
        get_user_model(), related_name='assigned_bugs', blank=True
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

    @property
    def status_tuples(self):
        """A list of tuples containing the status and its bootstrap class"""
        return [(s, self.STATUS_CLASSES[s]) for s in self.POSSIBLE_STATUS]

    @classmethod
    def get_active(cls):
        """Return a queryset with the active bugs"""
        return cls.objects.filter(_status__in=cls.ACTIVE_STATUS)

    def __str__(self):
        """Return the string representation of the bug object"""
        return self.title

    __repr__ = __str__


class Message(models.Model):
    """A message written on the bug board"""

    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='messages'
    )
    bug = models.ForeignKey(
        Bug, on_delete=models.CASCADE, related_name='messages'
    )
    creationDate = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        """Return the string representation of the message object"""
        result = self.writer.get_short_name() + ' - ' + self.message
        if len(result) > 32:
            result = result[:30] + '...'

        return result

    __repr__ = __str__
