from django.test import TestCase

from projects.models import Project


class ProjectModelTests(TestCase):
    """Test the project model"""

    def test_project_set_status(self):
        """Test the set_status project method"""
        proj = Project.objects.create(title='Test')

        proj.set_status('ON-GOING')
        self.assertEqual(proj.status, 'ON-GOING')

        with self.assertRaises(ValueError):
            proj.set_status('NON_EXISTING_ENUM')
