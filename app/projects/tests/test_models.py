from django.test import TestCase
from mixer.backend.django import mixer

from projects.models import Project
from bugs.models import Bug


class ProjectModelTests(TestCase):
    """Test the project model"""

    def setUp(self):
        self.project = Project.objects.create(title='Test')

    def test_project_status_enums(self):
        """Test the status enums are set up correctly"""
        for active_status in Project.ACTIVE_STATUS:
            self.assertIn(active_status, Project.POSSIBLE_STATUS)

        for status in Project.POSSIBLE_STATUS:
            self.assertIn(status, Project.STATUS_CLASSES.keys())

    def test_project_set_status(self):
        """Test the set_status project method"""
        self.project.set_status('ON-GOING')
        self.assertEqual(self.project.status, 'ON-GOING')

        with self.assertRaises(ValueError):
            self.project.set_status('NON_EXISTING_ENUM')

    def test_project_status_tuples(self):
        """Test the status_tuples property"""
        for st in self.project.status_tuples:
            self.assertEqual(Project.STATUS_CLASSES[st[0]], st[1])

    def test_project_get_active(self):
        """Test the get_active class method"""
        Project.objects.create(title='Test2', _status='PAUSED')
        Project.objects.create(title='Test3', _status='CLOSED')
        Project.objects.create(title='Test4', _status='FINISHED')

        actives = Project.get_active()

        self.assertQuerysetEqual(set(actives), {str(self.project)})

    def test_project_active_bugs(self):
        """Test the active_bugs project method"""
        project = mixer.blend(Project)
        b1 = mixer.blend(Bug, project=project, _status='WAITING')
        b2 = mixer.blend(Bug, project=project, _status='BEING WORKED')
        b3 = mixer.blend(Bug, project=project, _status='FIXED')
        b4 = mixer.blend(Bug, project=project, _status='CLOSED')
        active_bugs = project.active_bugs

        self.assertIn(b1, active_bugs)
        self.assertIn(b2, active_bugs)
        self.assertNotIn(b3, active_bugs)
        self.assertNotIn(b4, active_bugs)

        p2 = Project.objects.create(title="Proj")
        self.assertFalse(p2.active_bugs.exists())
