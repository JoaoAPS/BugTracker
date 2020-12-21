from django.test import SimpleTestCase
from django.urls import reverse, resolve

from bugs import views


class BugsUrlTests(SimpleTestCase):
    """The the bug related urls are correctly set up"""

    def test_bug_list_url(self):
        """Test the bug list view url"""
        url = reverse('bugs:list')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.BugListView)

    def test_bug_detail_url(self):
        """Test the bug detail view url"""
        url = reverse('bugs:detail', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.BugDetailView)

    def test_bug_create_url(self):
        """Test the bug create view url"""
        url = reverse('bugs:create')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.BugCreateView)

    def test_bug_update_url(self):
        """Test the bug update view url"""
        url = reverse('bugs:update', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.BugUpdateView)

    def test_bug_assign_member_url(self):
        """Test the bug assign_member view url"""
        url = reverse('bugs:assign_member', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.BugAssignMemberView)

    def test_bug_change_status_url(self):
        """Test the bug change_status view url"""
        url = reverse('bugs:change_status', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.BugChangeStatusView)

    def test_bug_change_working_status_url(self):
        """Test the bug change_working_status view url"""
        url = reverse('bugs:change_working_status', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.BugChangeWorkingStatusView)


class MessagesUrlTests(SimpleTestCase):
    """The the message related urls are correctly set up"""

    def test_message_create_url(self):
        """Test the message create url"""
        url = reverse('bugs:create_message', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.MessageCreateView)
