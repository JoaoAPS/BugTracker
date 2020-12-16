import pytest
from django.urls import reverse


@pytest.fixture
def project_list_url():
    return reverse('projects:list')


@pytest.fixture
def project_detail_url(project):
    return reverse('projects:detail', args=[project.id])


@pytest.fixture
def project_create_url():
    return reverse('projects:create')


@pytest.fixture
def project_update_url(project):
    return reverse('projects:update', args=[project.id])


@pytest.fixture
def project_add_member_url(project):
    return reverse('projects:add_member', args=[project.id])


@pytest.fixture
def project_add_supervisor_url(project):
    return reverse('projects:add_supervisor', args=[project.id])


@pytest.fixture
def project_change_status_url(project):
    return reverse('projects:change_status', args=[project.id])


@pytest.fixture
def project_url_names_to_fixtures(
    project_list_url,
    project_detail_url,
    project_create_url,
    project_update_url,
    project_add_member_url,
    project_add_supervisor_url,
    project_change_status_url,
):
    return {
        'project_list_url': project_list_url,
        'project_detail_url': project_detail_url,
        'project_create_url': project_create_url,
        'project_update_url': project_update_url,
        'project_add_member_url': project_add_member_url,
        'project_add_supervisor_url': project_add_supervisor_url,
        'project_change_status_url': project_change_status_url,
    }
