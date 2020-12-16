import pytest
from mixer.backend.django import mixer

from projects.models import Project


@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        email='admin@gotmail.com',
        name="Admin",
        password='Admin password'
    )


@pytest.fixture
def superuser_client(client, superuser):
    """A client with a superuser logged in"""
    client.force_login(superuser)
    return client


@pytest.fixture
def member(django_user_model):
    """A user that is not a member of any project"""
    return mixer.blend(django_user_model)


@pytest.fixture
def project_member(django_user_model):
    """A member of the project fixture"""
    return mixer.blend(django_user_model)


@pytest.fixture
def supervisor(django_user_model):
    """A supervisor of the project fixture"""
    return mixer.blend(django_user_model)


@pytest.fixture
def project(supervisor, project_member):
    project = mixer.blend(Project)
    project.members.add(project_member)
    project.members.add(supervisor)
    project.supervisors.add(supervisor)
    return project
