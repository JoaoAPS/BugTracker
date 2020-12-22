from django.test import TestCase
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from bugs.models import Bug, Message
from projects.models import Project


class BugModelTests(TestCase):
    """Test the bug model"""

    def setUp(self):
        self.member = get_user_model().objects.create_user(
            name='Test Member',
            email='test@gotmail.com',
            password='testpass'
        )
        self.proj = Project.objects.create(title='Test')
        self.bug = Bug.objects.create(
            title='Test', project=self.proj, creator=self.member
        )

    def test_bug_status_enums(self):
        """Test the bug status enums are set up correctly"""
        for active_status in Bug.ACTIVE_STATUS:
            self.assertIn(active_status, Bug.POSSIBLE_STATUS)

        self.assertIn(Bug.WAITING_STATUS, Bug.POSSIBLE_STATUS)
        self.assertIn(Bug.WORKING_STATUS, Bug.POSSIBLE_STATUS)

        for status in Bug.POSSIBLE_STATUS:
            self.assertIn(status, Bug.STATUS_CLASSES.keys())

    def test_bug_set_status(self):
        """Test the bug set_status method"""
        self.bug.set_status('FIXED')
        self.assertEqual(self.bug.status, 'FIXED')

        with self.assertRaises(ValueError):
            self.bug.set_status('NON_EXISTING_ENUM')

    def test_bug_status_tuples(self):
        """Test the bug status_tuples property"""
        for st in self.bug.status_tuples:
            self.assertEqual(Bug.STATUS_CLASSES[st[0]], st[1])

    def test_bug_get_active(self):
        """Test the bug get_active class method"""
        b1 = self.bug
        b2 = Bug.objects.create(
            title='Test2',
            project=self.proj,
            creator=self.member,
            _status='BEING WORKED'
        )
        Bug.objects.create(
            title='Test3',
            project=self.proj,
            creator=self.member,
            _status='CLOSED'
        )
        Bug.objects.create(
            title='Test4',
            project=self.proj,
            creator=self.member,
            _status='FIXED'
        )
        actives = Bug.get_active().order_by('title')

        self.assertQuerysetEqual(set(actives), [str(b1), str(b2)])


class MessageModelTest(TestCase):
    """Test the message model"""

    def test_message_str_representation(self):
        """Test the string representation of the message model"""
        member = mixer.blend(get_user_model(), name="John Barnabara")
        mes = mixer.blend(Message, writer=member, content="Short content")
        assert str(mes) == member.get_short_name() + ' - ' + mes.content

        mes = mixer.blend(
            Message,
            writer=member,
            content="A very long string that would occupy too much space if \
                we were to print it all as string"
        )
        assert len(str(mes)) == 32
        assert str(mes)[-3:] == '...'
