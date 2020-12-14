from django.test import SimpleTestCase
from django.urls import reverse, resolve

from core import views
from members.views import MemberProfileView


class CoreUrlTests(SimpleTestCase):
    """The the core urls are correctly set up"""

    def test_index_url(self):
        """Test the index view url"""
        url = reverse('index')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.IndexView)

    def test_member_profile_url(self):
        """Test the member profile view url"""
        url = reverse('member-profile')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, MemberProfileView)
