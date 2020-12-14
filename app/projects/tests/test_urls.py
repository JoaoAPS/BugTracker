from django.test import SimpleTestCase
from django.urls import reverse, resolve

from projects import views


class ProjectsUrlTests(SimpleTestCase):
    """The the project related urls are correctly set up"""

    def test_project_list_url(self):
        """Test the project list view url"""
        url = reverse('projects:list')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.ProjectListView)

    def test_project_detail_url(self):
        """Test the project detail view url"""
        url = reverse('projects:detail', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.ProjectDetailView)

    def test_project_create_url(self):
        """Test the project create view url"""
        url = reverse('projects:create')
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.ProjectCreateView)

    def test_project_update_url(self):
        """Test the project update view url"""
        url = reverse('projects:update', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.ProjectUpdateView)

    def test_project_add_member_url(self):
        """Test the project add_member view url"""
        url = reverse('projects:add_member', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.ProjectAddMemberView)

    def test_project_add_supervisor_url(self):
        """Test the project add_supervisor view url"""
        url = reverse('projects:add_supervisor', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.ProjectAddSupervisorView)

    def test_project_change_status_url(self):
        """Test the project change_status view url"""
        url = reverse('projects:change_status', args=[1])
        urlViewClass = resolve(url).func.view_class
        self.assertEqual(urlViewClass, views.ProjectChangeStatusView)
