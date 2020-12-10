from django.db import models

from members.models import Member


class Project(models.Model):
    """A project worked on by members and containing bugs"""
    POSSIBLE_STATUS = ['ON-GOING', 'CLOSED', 'FINISHED', 'PAUSED']
    STATUS_CLASSES = {
        'ON-GOING': 'primary',
        'CLOSED': 'danger',
        'FINISHED': 'success',
        'PAUSED': 'secondary'
    }
    ACTIVE_STATUS = ['ON-GOING']

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    _status = models.CharField(max_length=10, default='ON-GOING')
    creationDate = models.DateField(auto_now_add=True)
    closingDate = models.DateField(null=True, blank=True, default=None)

    members = models.ManyToManyField(
        Member, related_name='projects'
    )
    supervisors = models.ManyToManyField(
        Member, related_name='supervised_projects'
    )

    @property
    def status(self):
        return self._status

    def set_status(self, status):
        """Set the status of the project checking for valid status"""
        if status not in self.POSSIBLE_STATUS:
            possibleVals = str(self.POSSIBLE_STATUS).strip('[]')
            raise ValueError(
                'Project status must be one of the following: ' + possibleVals
            )

        self._status = status

    @classmethod
    def get_active(cls):
        """Return a queryset with the active projects"""
        return cls.objects.filter(_status__in=cls.ACTIVE_STATUS)

    @property
    def active_bugs(self):
        if not self.bugs.exists():
            return self.bugs
        return self.bugs.filter(_status__in=self.bugs.first().ACTIVE_STATUS)

    def __str__(self):
        """Return the string representation of the project object"""
        return self.title

    __repr__ = __str__
