from django.test import TestCase

from projects.models import Project


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

    def test_get_active(self):
        """Test the get_active class method"""
        Project.objects.create(title='Test2', _status='PAUSED')
        Project.objects.create(title='Test3', _status='CLOSED')
        Project.objects.create(title='Test4', _status='FINISHED')

        actives = Project.get_active()

        self.assertQuerysetEqual(set(actives), {str(self.project)})
