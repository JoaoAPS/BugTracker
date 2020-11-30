from django.test import TestCase
from django.contrib.auth import get_user_model

from bugs.models import Bug
from projects.models import Project


class BugModelTests(TestCase):
    """Test the bug model"""

    def test_bug_set_status(self):
        """Test the set_status project method"""
        member = get_user_model().objects.create_user(
            name='Test Member',
            email='test@gotmail.com',
            password='testpass'
        )
        proj = Project.objects.create(title='Test')

        bug = Bug.objects.create(title='Test', project=proj, creator=member)

        bug.set_status('FIXED')
        self.assertEqual(bug.status, 'FIXED')

        with self.assertRaises(ValueError):
            proj.set_status('NON_EXISTING_ENUM')
