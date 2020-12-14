from django.test import TestCase, Client
from django.urls import reverse

from core import utils
from bugs.models import Bug


class TestBugViewsPermissions(TestCase):
    """Test the bug views permission"""

    def setUp(self):
        self.client = Client()

        self.member = utils.sample_member()
        self.superuser = utils.sample_superuser()
        self.project = utils.sample_project()
        self.bug = utils.sample_bug(creator=self.member, project=self.project)

        self.list_url = reverse('bugs:list')
        self.detail_url = reverse('bugs:detail', args=[self.bug.id])
        self.create_url = reverse('bugs:create')
        self.update_url = reverse('bugs:update', args=[self.bug.id])
        self.assign_member_url = reverse(
            'bugs:assign_member', args=[self.bug.id]
        )
        self.change_status_url = reverse(
            'bugs:change_status', args=[self.bug.id]
        )
        self.change_working_status_url = reverse(
            'bugs:change_working_status', args=[self.bug.id]
        )

        self.bugPayload = {'title': 'Tmp', 'project': self.project.id}

    def test_unauthenticaded_requests(self):
        """Test the bug views for unauthenticated requests"""
        for url in [
            self.list_url,
            self.detail_url,
            self.create_url,
            self.update_url,
        ]:
            res = self.client.get(url)
            redirect_url = res.url.split('?')[0]

            self.assertEqual(res.status_code, 302)
            self.assertEqual(redirect_url, reverse('members:login'))

        for url in [
            self.create_url,
            self.update_url,
            self.assign_member_url,
            self.change_status_url,
            self.change_working_status_url,
        ]:
            res = self.client.post(url)
            redirect_url = res.url.split('?')[0]

            self.assertEqual(res.status_code, 302)
            self.assertEqual(redirect_url, reverse('members:login'))

    def test_superuser_requests(self):
        """Test the bug views for superuser requests"""
        self.client.force_login(self.superuser)

        for url in [
            self.list_url,
            self.detail_url,
            self.create_url,
            self.update_url,
        ]:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200)

        for url in [
            self.create_url,
            self.update_url,
            self.assign_member_url,
            self.change_status_url,
            self.change_working_status_url,
        ]:
            res = self.client.post(url)
            self.assertNotIn(res.status_code, [404, 403, 302])

    def test_project_supervisor_requests(self):
        """Test the bug views for project supervisors requests"""
        self.project.members.add(self.member)
        self.project.supervisors.add(self.member)
        self.client.force_login(self.member)

        for url in [
            self.list_url,
            self.detail_url,
            self.create_url,
            self.update_url,
        ]:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200)

        for url in [
            self.create_url,
            self.update_url,
            self.assign_member_url,
            self.change_status_url,
            self.change_working_status_url,
        ]:
            res = self.client.post(url)
            self.assertNotIn(res.status_code, [404, 403, 302])

    def test_project_member_requests(self):
        """Test the bug views for project members requests"""
        self.project.members.add(self.member)
        self.client.force_login(self.member)

        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 200)

        res = self.client.get(self.create_url)
        self.assertEqual(res.status_code, 200)

        res = self.client.get(self.update_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.create_url)
        self.assertNotIn(res.status_code, [404, 403, 302])

        res = self.client.post(self.update_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.assign_member_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.change_status_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.change_working_status_url)
        self.assertEqual(res.status_code, 403)

    def test_non_project_member_requests(self):
        """Test the bug views for project members requests"""
        self.client.force_login(self.member)

        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.get(self.create_url)
        self.assertEqual(res.status_code, 200)

        res = self.client.get(self.update_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.create_url, self.bugPayload)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.update_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.assign_member_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.change_status_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.change_working_status_url)
        self.assertEqual(res.status_code, 403)

    def test_assigned_member_requests(self):
        """Test the bug views for requests from members assigned to the bug"""
        res = self.client.post(self.change_working_status_url, {'starting': 1})
        self.assertEqual(res.status_code, 302)


class TestBugListView(TestCase):
    """Test the bug list view"""

    def setUp(self):
        self.list_url = reverse('bugs:list')

        self.member = utils.sample_member()
        self.project = utils.sample_project(creator=self.member)

        self.client = Client()
        self.client.force_login(self.member)

    def test_bug_list_GET_only(self):
        """Test only GET requests are allowed for list view"""
        res = self.client.post(self.list_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.patch(self.list_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.put(self.list_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.delete(self.list_url)
        self.assertEqual(res.status_code, 405)

    def test_bug_list_empty_list(self):
        """Test the bug list view when the bug list is empty"""
        res = self.client.get(self.list_url)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.context['bugs'].exists())
        self.assertContains(res, 'No bugs found')

    def test_bug_list_basic(self):
        """Test the bug list for a basic request"""
        b1 = utils.sample_bug(
            creator=self.member, project=self.project, title="Bug c"
        )
        b2 = utils.sample_bug(
            creator=self.member, project=self.project, title="Bug a"
        )
        utils.sample_bug(
            creator=self.member,
            project=self.project,
            title="Bug d",
            _status="FIXED"
        )
        utils.sample_bug(
            creator=self.member,
            project=self.project,
            title="Bug b",
            _status="CLOSED"
        )

        res = self.client.get(self.list_url)
        queryset = Bug.objects.filter(id__in=[b1.id, b2.id])

        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context['bugs'],
            [repr(bug) for bug in queryset.order_by('-creationDate')]
        )

    def test_bug_list_show_inactive(self):
        """Test the bug list for a request showing inactive bugs"""
        utils.sample_bug(
            creator=self.member, project=self.project, title="Bug c"
        )
        utils.sample_bug(
            creator=self.member, project=self.project, title="Bug a"
        )
        utils.sample_bug(
            creator=self.member,
            project=self.project,
            title="Bug d",
            _status="FIXED"
        )
        utils.sample_bug(
            creator=self.member,
            project=self.project,
            title="Bug b",
            _status="CLOSED"
        )

        queryset = Bug.objects.all().order_by('-creationDate')
        res = self.client.get(self.list_url + '?show_inactive=1')

        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context['bugs'],
            [repr(bug) for bug in queryset],
        )
