import pytest
from pytest_django.asserts import \
    assertRedirects  # , assertTemplateUsed, assertContains, assertNotContains
# from mixer.backend.django import mixer

from django.urls import reverse


# ----------- Permission Tests -----------
@pytest.mark.parametrize('method,url_name,should_succed', [
    ('get', 'member_list_url', False),
    ('get', 'member_detail_url', False),
    ('get', 'member_profile_url', False),
    ('get', 'member_register_url', False),
    ('get', 'member_login_url', True),
    ('post', 'member_register_url', False),
    ('post', 'member_login_url', True),
    ('post', 'member_logout_url', False),
])
def test_member_views_unauthenticated_permissions(
    client, member_url_names_to_fixtures, method, url_name, should_succed
):
    """Test unathorized requests cannot access member views"""
    url = member_url_names_to_fixtures[url_name]
    res = getattr(client, method)(url)

    if should_succed:
        assert res.status_code == 200
    else:
        assertRedirects(res, reverse('members:login') + '?next=' + url)


@pytest.mark.parametrize('method,url_name', [
    ('get', 'member_list_url'),
    ('get', 'member_detail_url'),
    ('get', 'member_profile_url'),
    ('get', 'member_register_url'),
    ('get', 'member_login_url'),
    ('post', 'member_register_url'),
    ('post', 'member_login_url'),
    ('post', 'member_logout_url'),
])
def test_member_views_superuser_permissions(
    superuser_client, member_url_names_to_fixtures, method, url_name
):
    """Test superuser request permission are correctly set up"""
    url = member_url_names_to_fixtures[url_name]
    res = getattr(superuser_client, method)(url)

    assert res.status_code in [200, 302, 400]


@pytest.mark.parametrize('method,url_name,should_succed', [
    ('get', 'member_list_url', True),
    ('get', 'member_detail_url', True),
    ('get', 'member_profile_url', True),
    ('get', 'member_register_url', False),
    ('get', 'member_login_url', True),
    ('post', 'member_register_url', False),
    ('post', 'member_login_url', True),
    ('post', 'member_logout_url', True),
])
def test_member_views_member_permissions(
    member_client,
    member_url_names_to_fixtures,
    method,
    url_name,
    should_succed
):
    """Test member request permission are correctly set up"""
    url = member_url_names_to_fixtures[url_name]
    res = getattr(member_client, method)(url)

    if should_succed:
        assert res.status_code in [200, 302, 400]
    else:
        assert res.status_code == 403


@pytest.mark.parametrize('url_name,allowed_methods', [
    ('member_list_url', ['GET']),
    ('member_detail_url', ['GET']),
    ('member_profile_url', ['GET']),
    ('member_register_url', ['GET', 'POST', 'PUT']),
    ('member_login_url', ['GET', 'POST', 'PUT']),
    ('member_logout_url', ['POST']),
])
def test_member_views_allowed_methods(
    superuser_client,
    member_url_names_to_fixtures,
    url_name,
    allowed_methods
):
    """Test the member views only allow the assigned methods"""
    url = member_url_names_to_fixtures[url_name]

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
