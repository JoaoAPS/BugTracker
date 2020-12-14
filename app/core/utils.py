from django.contrib.auth import get_user_model

from projects.models import Project
from bugs.models import Bug


def sample_member(**kwargs):
    """Create and return a sample member"""
    arguments = {
        'email': 'sample_user@gotmail.com',
        'name': 'Sample Member',
        'password': 'testpass'
    }
    arguments.update(**kwargs)

    return get_user_model().objects.create_user(**arguments)


def sample_superuser(**kwargs):
    """Create and return a sample superuser"""
    arguments = {
        'email': 'sample_superuser@gotmail.com',
        'name': 'Sample Member',
        'password': 'testpass'
    }
    arguments.update(**kwargs)

    return get_user_model().objects.create_superuser(**arguments)


def sample_project(creator=None, **kwargs):
    """Create and return a sample project"""
    arguments = {
        'title': 'Sample Project',
        'description': 'To be used for testing - project'
    }
    arguments.update(**kwargs)

    project = Project.objects.create(**arguments)
    if creator:
        project.creator = creator

    return project


def sample_bug(creator, project, **kwargs):
    """Create and return a sample bug"""
    arguments = {
        'title': 'Sample Bug',
        'description': 'To be used for testing - bug'
    }
    arguments.update(**kwargs)
    arguments.update({'creator': creator, 'project': project})

    return Bug.objects.create(**arguments)
