from django.test import TestCase

from projects.models import Project


class ProjectModelPositiveTests(TestCase):
    """Test the project model for successful operations"""

    def test_project_setStatus(self):
        """Test the setStatus project method"""
        proj = Project.objects.create(title='Test')

        proj.set_status('ON-GOING')
        self.assertEqual(proj.status, 'ON-GOING')

        with self.assertRaises(ValueError):
            proj.set_status('NON_EXISTING_ENUM')
