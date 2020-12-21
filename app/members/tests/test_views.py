import pytest
from pytest_django.asserts import \
    assertRedirects, assertTemplateUsed, assertContains, assertNotContains
from mixer.backend.django import mixer

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
    ('member_logout_url', ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']),
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


# ----------- List View Tests -----------
def test_member_list_view_basic(
    django_user_model,
    member_client,
    member,
    member_list_url,
):
    """Test the member list view for a basic request"""
    mixer.blend(django_user_model)
    mixer.blend(django_user_model)

    res = member_client.get(member_list_url)
    context_members = res.context['members'].order_by('id')
    database_members = django_user_model.objects.all().order_by('id')

    assert res.status_code == 200
    assertTemplateUsed(res, 'members/list.html')
    assert list(context_members) == list(database_members)


def test_member_list_view_show_register_link_when_admin(
    client,
    member,
    superuser,
    member_list_url,
    member_register_url,
):
    """Test member list view shows link to registration if admin request"""
    client.force_login(member)
    res = client.get(member_list_url)
    assertNotContains(res, member_register_url)

    client.force_login(superuser)
    res = client.get(member_list_url)
    assertContains(res, member_register_url)


# ----------- Detail View Tests -----------
def test_member_detail_404_on_inexistent_member(supervisor_client):
    """Test member detail view raises 404 when requested inexistent member"""
    url = reverse('members:detail', args=[124214])
    res = supervisor_client.get(url)
    assert res.status_code == 404


def test_member_detail_successful_request(
    supervisor_client, member_detail_url, member
):
    """Test a successful request on the member detail view"""
    res = supervisor_client.get(member_detail_url)

    assert res.status_code == 200
    assertTemplateUsed(res, 'members/detail.html')
    assert res.context['member'] == member
    assertContains(res, member.name)


# ----------- Register View Tests -----------
def test_member_register_view_GET(superuser_client, member_register_url):
    """Test successfully GETting member register view with form"""
    res = superuser_client.get(member_register_url)

    assert res.status_code == 200
    assertTemplateUsed(res, 'registration/register.html')

    assertContains(res, 'Name')
    assertContains(res, 'Email')
    assertContains(res, 'Password')


def test_member_register_view_POST_successful(
    django_user_model, superuser_client, member_register_url
):
    """Test a member is registered when a valid request is made"""
    payload = {
        'name': 'Test Member',
        'email': 'test@mail.com',
        'password': 'passsss',
        'password2': 'passsss',
    }
    res = superuser_client.post(member_register_url, payload)

    assert res.status_code == 302
    member = django_user_model.objects.filter(email=payload['email'])
    assert member.exists()
    assert member[0].check_password(payload['password'])


@pytest.mark.parametrize('payload', [
    {},
    {
        'name': 'Name',
        'password': 'A_valid_pass',
        'password2': 'A_valid_pass',
    },
    {
        'email': 'name@mail.com',
        'password': 'A_valid_pass',
        'password2': 'A_valid_pass',
    },
    {
        'name': 'Name',
        'email': 'name@mail.com',
        'password2': 'A_valid_pass',
    },
    {
        'name': 'Name',
        'email': 'name@mail.com',
        'password': 'A_valid_pass',
    },
    {
        'name': '',
        'email': 'name@mail.com',
        'password': 'A_valid_pass',
        'password2': 'A_valid_pass',
    },
    {
        'name': 'Name',
        'email': '',
        'password': 'A_valid_pass',
        'password2': 'A_valid_pass',
    },
    {
        'name': 'Name',
        'email': 'name@mail.com',
        'password': '',
        'password2': '',
    },
    {
        'name': 'Name',
        'email': 'not_a_mail.com',
        'password': 'A_valid_pass',
        'password2': 'A_valid_pass',
    },
    {
        'name': 'Name',
        'email': 'name@mail.com',
        'password': 'A_valid_pass',
        'password2': 'Wrong_password2',
    },
])
def test_member_register_invalid_payload(
    django_user_model, superuser_client, member_register_url, payload
):
    """Test member register view does not register member if invalid payload"""
    num_member_before = django_user_model.objects.count()

    res = superuser_client.post(member_register_url, payload)
    payload.pop('password', None)
    payload.pop('password2', None)

    assert res.status_code == 200
    assert num_member_before == django_user_model.objects.count()


# ----------- Profile View Tests -----------
def test_member_profile_successful_request(
    django_user_model, client, member_profile_url
):
    """Test a successful request on the member profile view"""
    member = mixer.blend(django_user_model)
    client.force_login(member)
    res = client.get(member_profile_url)

    assert res.status_code == 200
    assertTemplateUsed(res, 'members/profile.html')
    assert res.context['member'] == member
    assertContains(res, member.get_short_name())
