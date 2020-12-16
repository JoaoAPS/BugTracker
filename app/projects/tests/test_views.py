import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse


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
