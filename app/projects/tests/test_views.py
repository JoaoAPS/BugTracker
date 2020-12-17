import pytest
from pytest_django.asserts import \
    assertRedirects, assertTemplateUsed, assertContains, assertNotContains
from mixer.backend.django import mixer
import datetime

from django.urls import reverse

from projects.models import Project


# ----------- Permission Tests -----------
@pytest.mark.parametrize('method,url_name', [
    ('get', 'project_list_url'),
    ('get', 'project_detail_url'),
    ('get', 'project_create_url'),
    ('get', 'project_update_url'),
    ('post', 'project_create_url'),
    ('post', 'project_update_url'),
    ('post', 'project_add_member_url'),
    ('post', 'project_add_supervisor_url'),
    ('post', 'project_change_status_url'),
])
def test_project_views_unauthenticated_permissions(
    client, project_url_names_to_fixtures, method, url_name
):
    """Test unathorized requests cannot access project views"""
    url = project_url_names_to_fixtures[url_name]
    res = getattr(client, method)(url)

    assertRedirects(res, reverse('members:login') + '?next=' + url)


@pytest.mark.parametrize('method,url_name', [
    ('get', 'project_list_url'),
    ('get', 'project_detail_url'),
    ('get', 'project_create_url'),
    ('get', 'project_update_url'),
    ('post', 'project_create_url'),
    ('post', 'project_update_url'),
    ('post', 'project_add_member_url'),
    ('post', 'project_add_supervisor_url'),
    ('post', 'project_change_status_url'),
])
def test_project_views_superuser_permissions(
    superuser_client, project_url_names_to_fixtures, method, url_name
):
    """Test superuser request permission are correctly set up"""
    url = project_url_names_to_fixtures[url_name]
    res = getattr(superuser_client, method)(url)

    assert res.status_code in [200, 400]


@pytest.mark.parametrize('method,url_name', [
    ('get', 'project_list_url'),
    ('get', 'project_detail_url'),
    ('get', 'project_create_url'),
    ('get', 'project_update_url'),
    ('post', 'project_create_url'),
    ('post', 'project_update_url'),
    ('post', 'project_add_member_url'),
    ('post', 'project_add_supervisor_url'),
    ('post', 'project_change_status_url'),
])
def test_project_views_supervisor_permissions(
    client, supervisor, project_url_names_to_fixtures, method, url_name
):
    """Test supervisor request permission are correctly set up"""
    client.force_login(supervisor)
    url = project_url_names_to_fixtures[url_name]
    res = getattr(client, method)(url)

    assert res.status_code in [200, 400]


@pytest.mark.parametrize('method,url_name,should_succed', [
    ('get', 'project_list_url', True),
    ('get', 'project_detail_url', True),
    ('get', 'project_create_url', True),
    ('get', 'project_update_url', False),
    ('post', 'project_create_url', True),
    ('post', 'project_update_url', False),
    ('post', 'project_add_member_url', False),
    ('post', 'project_add_supervisor_url', False),
    ('post', 'project_change_status_url', False),
])
def test_project_views_project_member_permissions(
    client,
    project_member,
    project_url_names_to_fixtures,
    method,
    url_name,
    should_succed
):
    """Test project member request permission are correctly set up"""
    client.force_login(project_member)
    url = project_url_names_to_fixtures[url_name]
    res = getattr(client, method)(url)

    if should_succed:
        assert res.status_code in [200, 400]
    else:
        assert res.status_code == 403


@pytest.mark.parametrize('method,url_name,should_succed', [
    ('get', 'project_list_url', True),
    ('get', 'project_detail_url', False),
    ('get', 'project_create_url', True),
    ('get', 'project_update_url', False),
    ('post', 'project_create_url', True),
    ('post', 'project_update_url', False),
    ('post', 'project_add_member_url', False),
    ('post', 'project_add_supervisor_url', False),
    ('post', 'project_change_status_url', False),
])
def test_project_views_non_project_member_permissions(
    client,
    member,
    project_url_names_to_fixtures,
    method,
    url_name,
    should_succed
):
    """Test non project member request permission are correctly set up"""
    client.force_login(member)
    url = project_url_names_to_fixtures[url_name]
    res = getattr(client, method)(url)

    if should_succed:
        assert res.status_code in [200, 400]
    else:
        assert res.status_code == 403


@pytest.mark.parametrize('url_name,allowed_methods', [
    ('project_list_url', ['GET']),
    ('project_detail_url', ['GET']),
    ('project_create_url', ['GET', 'POST', 'PUT']),
    ('project_update_url', ['GET', 'POST', 'PUT']),
    ('project_add_member_url', ['POST']),
    ('project_add_supervisor_url', ['POST']),
    ('project_change_status_url', ['POST']),
])
def test_project_views_allowed_methods(
    superuser_client,
    project_url_names_to_fixtures,
    url_name,
    allowed_methods
):
    """Test the project views only allow the assigned methods"""
    url = project_url_names_to_fixtures[url_name]

    res = superuser_client.get(url)
    was_allowed = res.status_code != 405
    assert was_allowed == ('GET' in allowed_methods)

    res = superuser_client.post(url)
    was_allowed = res.status_code != 405
    assert was_allowed == ('POST' in allowed_methods)

    res = superuser_client.put(url)
    was_allowed = res.status_code != 405
    assert was_allowed == ('PUT' in allowed_methods)

    res = superuser_client.patch(url)
    was_allowed = res.status_code != 405
    assert was_allowed == ('PATCH' in allowed_methods)

    res = superuser_client.delete(url)
    was_allowed = res.status_code != 405
    assert was_allowed == ('DELETE' in allowed_methods)


# ----------- List View Tests -----------
def test_project_list_view_empty_list(supervisor_client, project_list_url):
    """Test the project list view when there are not projects created"""
    assert not Project.objects.exists()

    res = supervisor_client.get(project_list_url)

    assert res.status_code == 200
    assertTemplateUsed(res, 'projects/list.html')
    assert not res.context['projects'].exists()
    assertContains(res, 'No projects found')


def test_project_list_view_basic(
    supervisor_client, project_list_url, project_create_url
):
    """Test the project list view for a basic request"""
    p1 = mixer.blend(Project)
    p2 = mixer.blend(Project)
    mixer.blend(Project, _status='CLOSED')
    mixer.blend(Project, _status='FINISHED')

    res = supervisor_client.get(project_list_url)
    context_projects = res.context['projects']

    assert res.status_code == 200
    assertTemplateUsed(res, 'projects/list.html')
    assertContains(res, project_create_url)

    assert context_projects.count() == 2
    assert p1 in context_projects
    assert p2 in context_projects


def test_project_list_view_show_inactive(supervisor_client, project_list_url):
    """Test the project list view shows inactive projects when asked"""
    mixer.blend(Project)
    mixer.blend(Project)
    mixer.blend(Project, _status='CLOSED')
    mixer.blend(Project, _status='FINISHED')

    res = supervisor_client.get(project_list_url + '?show_inactive=1')
    context_projects = res.context['projects']

    assert res.status_code == 200
    assertTemplateUsed(res, 'projects/list.html')
    assert context_projects.count() == 4


# ----------- Detail View Tests -----------
def test_project_detail_404_on_inexistent_project(
    supervisor_client
):
    """Test project detail view raises 404 when requested inexistent project"""
    url = reverse('projects:detail', args=[124214])
    res = supervisor_client.get(url)
    assert res.status_code == 404


def test_project_detail_successful_request(
    supervisor_client, project_detail_url, project
):
    """Test a successful request on the project detail view"""
    res = supervisor_client.get(project_detail_url)

    assert res.status_code == 200
    assertTemplateUsed(res, 'projects/detail.html')
    assert res.context['project'] == project

    assertContains(res, project.title)
    assertContains(res, project.description.replace('\n', '<br>'))
    assertContains(res, str.title(project.status))
    assertContains(res, reverse('bugs:create'))


def test_project_detail_supervisor_buttons(
    superuser_client,
    supervisor_client,
    client,
    project_member,
    project_detail_url,
    project_update_url,
    project_add_member_url,
    project_add_supervisor_url,
):
    res = superuser_client.get(project_detail_url)

    assertContains(res, project_update_url)
    assertContains(res, project_add_member_url)
    assertContains(res, project_add_supervisor_url)

    res = supervisor_client.get(project_detail_url)
    assertContains(res, project_update_url)
    assertContains(res, project_add_member_url)
    assertContains(res, project_add_supervisor_url)

    client.force_login(project_member)
    res = client.get(project_detail_url)
    assertNotContains(res, project_update_url)
    assertNotContains(res, project_add_member_url)
    assertNotContains(res, project_add_supervisor_url)


# ----------- Create View Tests -----------
def test_project_create_view_GET(member_client, project_create_url):
    """Test successfully GETting project create view with form"""
    res = member_client.get(project_create_url)

    assert res.status_code == 200
    assertTemplateUsed(res, 'projects/create.html')

    assertContains(res, 'Title')
    assertContains(res, 'Description')
    assertContains(res, 'Members')


def test_project_create_view_POST_successful(
    django_user_model, member_client, project_create_url
):
    """Test a project is created when a valid request is made to create view"""
    m1 = mixer.blend(django_user_model)
    m2 = mixer.blend(django_user_model)

    payload = {
        'title': 'Test Project 142',
        'description': 'A descriptione',
        'members': [m1.id, m2.id]
    }
    res = member_client.post(project_create_url, payload)
    payload.pop('members')

    assert res.status_code == 302
    project = Project.objects.filter(**payload)
    assert project.exists()
    assert m1 in project[0].members.all()
    assert m2 in project[0].members.all()


def test_project_create_view_sets_fields_automatically(
    client, member, project_create_url
):
    """Test creationDate is set and creator is set as supervisor and member"""
    payload = {'title': 'Test Project 142'}

    client.force_login(member)
    res = client.post(project_create_url, payload)

    assert res.status_code == 302
    project = Project.objects.get(**payload)

    assert member in project.members.all()
    assert member in project.supervisors.all()
    assert project.creationDate.date() == datetime.date.today()


def test_project_create_invalid_payload(
    member_client, project_create_url
):
    """Test project create view does not create project if invalid payload"""
    assert not Project.objects.exists()

    res = member_client.post(project_create_url)
    assert res.status_code == 200
    assert not Project.objects.exists()

    res = member_client.post(project_create_url, {'description': 'Something'})
    assert res.status_code == 200
    assert not Project.objects.exists()

    res = member_client.post(project_create_url, {'title': ''})
    assert res.status_code == 200
    assert not Project.objects.exists()

    res = member_client.post(
        project_create_url, {'title': 'Title', 'members': [126478]}
    )
    assert res.status_code == 200
    assert not Project.objects.exists()


# ----------- Update View Tests -----------
def test_project_update_view_GET(
    supervisor_client, project, project_update_url, project_change_status_url
):
    """Test GETting project update view with no optinal parameters"""
    res = supervisor_client.get(project_update_url)

    assert res.status_code == 200
    assertTemplateUsed(res, 'projects/update.html')

    assertContains(res, 'Title')
    assertContains(res, project.title)

    assertContains(res, 'Description')
    assertContains(res, project.description)

    assertContains(res, 'Members')
    assertContains(res, 'Supervisors')

    assertContains(res, project_change_status_url)


def test_project_update_view_POST_successful(
    django_user_model,
    supervisor_client,
    project,
    project_update_url,
):
    """Test POSTing project update view with correct payload"""
    m1 = mixer.blend(django_user_model)
    m2 = mixer.blend(django_user_model)
    project.members.add(m1)

    payload = {
        'title': 'New Title',
        'description': 'New description',
        'members': [m1.id, m2.id],
        'supervisors': [m1.id]
    }
    res = supervisor_client.post(project_update_url, payload)

    project.refresh_from_db()
    members = django_user_model.objects.filter(
        id__in=payload['members']
    ).order_by('id')
    supervisors = django_user_model.objects.filter(
        id__in=payload['supervisors']
    ).order_by('id')

    assert res.status_code == 302
    assert project.title == payload['title']
    assert project.description == payload['description']
    assert list(project.members.order_by('id')) == list(members)
    assert list(project.supervisors.order_by('id')) == list(supervisors)


@pytest.mark.parametrize('payload', [
    {'title': ''},
    {'members': [12425]},
    {'supervisors': [12425]},
])
def test_project_update_view_POST_invalid_payload(
    django_user_model,
    supervisor_client,
    project,
    project_update_url,
    payload
):
    """Test an invalid payload to project update view doesn't update project"""
    res = supervisor_client.post(project_update_url, payload)
    updated_project = Project.objects.get(id=project.id)

    assert res.status_code == 200
    assert updated_project == project


# ----------- AddMember View Tests -----------
def test_project_add_member_view_successful(
    django_user_model, supervisor_client, project_add_member_url, project
):
    """Test project add_member view successfully adds members to project"""
    m0 = mixer.blend(django_user_model)
    m1 = mixer.blend(django_user_model)
    m2 = mixer.blend(django_user_model)
    project.members.add(m0)

    payload = {'member_ids': [m1.id, m2.id]}
    res = supervisor_client.post(project_add_member_url, payload)
    project.refresh_from_db()

    assert res.status_code == 302
    assert m0 in project.members.all()
    assert m1 in project.members.all()
    assert m2 in project.members.all()


@pytest.mark.parametrize('payload', [
    {},
    {'member_ids': 0},
    {'member_ids': [123]},
    {'member_ids': 'string'},
    {'member_ids': ['string']},
])
def test_project_add_member_view_invalid_payload(
    supervisor_client, project_add_member_url, project, payload
):
    """Test project add_member view handles invalid payload correctly"""
    res = supervisor_client.post(project_add_member_url, payload)
    updated_project = Project.objects.get(id=project.id)

    assert res.status_code == 400
    assert list(updated_project.members.all()) == list(project.members.all())


# ----------- AddSupervisor View Tests -----------
def test_project_add_supervisor_view_successful(
    django_user_model, supervisor_client, project_add_supervisor_url, project
):
    """Test project add_supervisor view successfully adds supervisors"""
    m0 = mixer.blend(django_user_model)
    m1 = mixer.blend(django_user_model)
    project.members.add(m0)
    project.members.add(m1)
    project.supervisors.add(m0)

    payload = {'supervisor_ids': [m1.id]}
    res = supervisor_client.post(project_add_supervisor_url, payload)
    project.refresh_from_db()

    assert res.status_code == 302
    assert m0 in project.supervisors.all()
    assert m1 in project.supervisors.all()


@pytest.mark.parametrize('payload', [
    {},
    {'supervisor_ids': 0},
    {'supervisor_ids': [123]},
    {'supervisor_ids': 'string'},
    {'supervisor_ids': ['string']},
])
def test_project_add_supervisor_view_invalid_payload(
    supervisor_client, project_add_supervisor_url, project, payload
):
    """Test project add_supervisor view handles invalid payload correctly"""
    res = supervisor_client.post(project_add_supervisor_url, payload)
    updated_project = Project.objects.get(id=project.id)

    assert res.status_code == 400
    assert list(updated_project.supervisors.all()) == \
        list(project.supervisors.all())


# ----------- ChangeStatus View Tests -----------
@pytest.mark.parametrize(
    'status', ['ON-GOING', 'FINISHED', 'PAUSED', 'CLOSED']
)
def test_project_change_status_view_successful(
    supervisor_client, project_change_status_url, project, status
):
    """Test project change_status view succesfully changes status"""
    res = supervisor_client.post(project_change_status_url, {'status': status})
    project.refresh_from_db()

    assert res.status_code == 302
    assert project.status == status


@pytest.mark.parametrize('payload', [
    {},
    {'status': 2},
    {'status': 'wrong status'},
])
def test_project_change_status_view_invalid_payload(
    supervisor_client, project_change_status_url, project, payload
):
    """Test project change_status handles invalid payload correctly"""
    res = supervisor_client.post(project_change_status_url, payload)
    updated_project = Project.objects.get(id=project.id)

    assert res.status_code == 400
    assert updated_project.status == project.status
