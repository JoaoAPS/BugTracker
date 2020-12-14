from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from members.models import Member


class MemberModelPositiveTests(TestCase):
    """Test the member model for successful operations"""

    def setUp(self):
        # Basic member
        self.name = 'Test User'
        self.email = 'test@gotmail.com'
        self.password = 'testpass'
        self.user = get_user_model().objects.create_user(
            name=self.name,
            email=self.email,
            password=self.password
        )

        # Admin member
        self.admin_name = 'Admin',
        self.admin_email = 'admin@gotmail.com'
        self.admin_password = 'adminpass'
        self.admin = get_user_model().objects.create_superuser(
            name=self.admin_name,
            email=self.admin_email,
            password=self.admin_password
        )

    def test_using_correct_user_model(self):
        """Test the default user model is the custom Member class"""
        self.assertEqual(get_user_model(), Member)

    def test_create_basic_member_positive(self):
        """Test creating a member object"""
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertTrue(self.user.check_password(self.password))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)

        inactive_user = get_user_model().objects.create_user(
            name=self.name,
            email='somemail@gotmail.com',
            password=self.password,
            is_active=False
        )
        self.assertFalse(inactive_user.is_active)

    def test_create_admin_member_positive(self):
        """Test creating a member object with admin privileges"""
        self.assertEqual(self.admin.name, self.admin_name)
        self.assertEqual(self.admin.email, self.admin_email)
        self.assertTrue(self.admin.check_password(self.admin_password))
        self.assertTrue(self.admin.is_active)
        self.assertTrue(self.admin.is_superuser)

    def test_authenticate_user(self):
        """Test authenticating an user"""
        auth_user = authenticate(username=self.email, password=self.password)
        self.assertEqual(auth_user, self.user)


class MemberModelNegativeTestes(TestCase):
    """Test the member model for unsuccessful operations"""

    def test_create_member_invalid_payload_negative(self):
        """Test creating a member with invalid info results in an error"""
        payloads = [
            {'email': 'mail@gotmail.com', 'password': 'testpass'},
            {'name': 'Test Name', 'password': 'testpass'},
            {'name': 'Test Name', 'email': 'mail@gotmail.com'},
        ]

        for payload in payloads:
            with self.assertRaises(TypeError):
                get_user_model().objects.create_user(**payload)
            with self.assertRaises(TypeError):
                get_user_model().objects.create_superuser(**payload)

        payloads = [
            {'name': '', 'email': 'mail@gotmail.com', 'password': 'testpass'},
            {'name': 'Test Name', 'email': '', 'password': 'testpass'},
            {'name': 'Test Name', 'email': 'mail@gotmail.com', 'password': ''},
        ]

        for payload in payloads:
            with self.assertRaises(ValueError):
                get_user_model().objects.create_user(**payload)
            with self.assertRaises(ValueError):
                get_user_model().objects.create_superuser(**payload)

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                name='Test Name',
                email='invalidmail.com',
                password='testpass'
            )

    def test_create_member_existing_email_negative(self):
        """Test email is not yet registered on creation"""
        user1 = get_user_model().objects.create_user(
            email='user@gotmail.com',
            name='User 1',
            password='123'
        )

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                email=user1.email,
                name='User 2',
                password='321'
            )


class MemberMethodTests(TestCase):

    def test_get_short_name(self):
        """Test the get_short_name method"""
        user1 = Member.objects.create_user(
            name='John Doe',
            email='user1@mail.com',
            password='123'
        )
        user2 = Member.objects.create_user(
            name='Valentina Johnson',
            email='user2@mail.com',
            password='123'
        )
        user3 = Member.objects.create_user(
            name='Dr. Haha Junior',
            email='user3@mail.com',
            password='123'
        )
        user4 = Member.objects.create_user(
            name='Superlongusername Last Name',
            email='user4@mail.com',
            password='123'
        )

        self.assertEqual(user1.get_short_name(), 'John Doe')
        self.assertEqual(user2.get_short_name(), 'Valentina')
        self.assertEqual(user3.get_short_name(), 'Dr. Haha')
        self.assertEqual(user4.get_short_name(), 'Superlongusername')
