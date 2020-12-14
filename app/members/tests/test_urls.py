from django.test import SimpleTestCase
from django.urls import reverse, resolve

from members import views


class MembersUrlTests(SimpleTestCase):
    """The the member related urls are correctly set up"""

    def test_member_list_url(self):
        """Test the member list view url"""
        url = reverse('members:list')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.MemberListView)

    def test_member_detail_url(self):
        """Test the member detail view url"""
        url = reverse('members:detail', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.MemberDetailView)

    def test_member_register_url(self):
        """Test the member register view url"""
        url = reverse('members:register')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.MemberCreateView)

    def test_member_login_url(self):
        """Test the member login view url"""
        url = reverse('members:login')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.MemberLoginView)

    def test_member_logout_url(self):
        """Test the member logout view url"""
        url = reverse('members:logout')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.MemberLogoutView)
