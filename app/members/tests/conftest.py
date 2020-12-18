import pytest

from django.urls import reverse


@pytest.fixture
def member_list_url():
    return reverse('members:list')


@pytest.fixture
def member_detail_url(member):
    return reverse('members:detail', args=[member.id])


@pytest.fixture
def member_register_url():
    return reverse('members:register')


@pytest.fixture
def member_profile_url():
    return reverse('member-profile')


@pytest.fixture
def member_login_url():
    return reverse('members:login')


@pytest.fixture
def member_logout_url():
    return reverse('members:logout')


@pytest.fixture
def member_url_names_to_fixtures(
    member_list_url,
    member_detail_url,
    member_register_url,
    member_profile_url,
    member_login_url,
    member_logout_url,
):
    return {
        'member_list_url': member_list_url,
        'member_detail_url': member_detail_url,
        'member_register_url': member_register_url,
        'member_profile_url': member_profile_url,
        'member_login_url': member_login_url,
        'member_logout_url': member_logout_url,
    }
