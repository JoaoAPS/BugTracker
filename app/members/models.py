from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.db import models


class MemberManager(BaseUserManager):
    """Manages the Member objects"""

    def create_user(self, name, email, password, **extra_fields):
        """Create a new non-admin user"""
        if not name or not email or not password:
            raise ValueError('A name, email and password must be provided')

        validate_email(email)

        defaults = {'is_active': True}
        defaults.update(**extra_fields, is_staff=False, is_superuser=False)

        member = Member(
            name=name,
            email=self.normalize_email(email),
            **defaults,
        )
        member.set_password(password)
        member.save()

        return member

    def create_superuser(self, name, email, password, **extra_fields):
        """Create a new admin user"""
        if not name or not email or not password:
            raise ValueError('A name, email and password must be provided')

        validate_email(email)

        defaults = {'is_active': True}
        defaults.update(**extra_fields, is_staff=True, is_superuser=True)

        member = Member(
            name=name,
            email=self.normalize_email(email),
            **defaults,
        )
        member.set_password(password)
        member.save()

        return member


class Member(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField('Email address', unique=True)
    username = None

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_short_name(self):
        """Return the first name of the member"""
        return self.name.split(' ')[0]

    def get_full_name(self):
        """Return the full name of the member"""
        return self.name

    __str__ = get_full_name
    __repr__ = get_full_name
