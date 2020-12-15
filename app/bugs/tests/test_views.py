import datetime

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
        self.assertTemplateUsed(res, 'bugs/list.html')
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
        self.assertTemplateUsed(res, 'bugs/list.html')
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
        self.assertTemplateUsed(res, 'bugs/list.html')
        self.assertQuerysetEqual(
            res.context['bugs'],
            [repr(bug) for bug in queryset],
        )


class TestBugDetailView(TestCase):
    """Test the bug detail view"""

    def setUp(self):
        self.superuser = utils.sample_superuser(email='super@mail.com')
        self.supervisor = utils.sample_member(email='email1@mail.com')
        self.creator = utils.sample_member(email='email2@mail.com')
        self.assigned = utils.sample_member(email='email3@mail.com')
        self.member = utils.sample_member(email='email4@mail.com')

        self.project = utils.sample_project(creator=self.supervisor)
        self.project.members.add(self.supervisor)
        self.project.members.add(self.creator)
        self.project.members.add(self.assigned)
        self.project.members.add(self.member)
        self.project.supervisors.add(self.supervisor)

        self.bug = utils.sample_bug(creator=self.creator, project=self.project)
        self.bug.assigned_members.add(self.assigned)

        self.client = Client()
        self.detail_url = reverse('bugs:detail', args=[self.bug.id])

    def test_bug_detail_only_GET(self):
        """Test only GET requests are allowed for the bug detail view"""
        self.client.force_login(self.supervisor)

        res = self.client.post(self.detail_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.patch(self.detail_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.put(self.detail_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, 405)

    def test_bug_detail_404_on_nonexisting_bug(self):
        """Test trying to access a non existing bug returns a 404"""
        self.client.force_login(self.supervisor)

        nonexisting_url = reverse('bugs:detail', args=[9876])
        res = self.client.get(nonexisting_url)

        self.assertEqual(res.status_code, 404)

    def test_bug_detail_successful_request(self):
        """Test a succesful request returns all necessary components"""
        self.client.force_login(self.supervisor)
        res = self.client.get(self.detail_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'bugs/detail.html')
        self.assertEqual(res.context['bug'], self.bug)
        self.assertContains(res, self.bug.title)
        self.assertContains(res, self.bug.description)
        self.assertContains(res, str.title(self.bug.status))

    def test_bug_detail_work_on_bug_button_for_assigned_only(self):
        """Test the 'Work on bug' button only appears for assigned members"""
        self.bug.set_status(self.bug.WAITING_STATUS)

        self.client.force_login(self.assigned)
        res = self.client.get(self.detail_url)
        self.assertContains(res, 'Work on bug')

        self.client.force_login(self.member)
        res = self.client.get(self.detail_url)
        self.assertNotContains(res, 'Work on bug')

    def test_bug_detail_assign_member_button_for_supervisors_only(self):
        """Test the 'Assign member' button only appears for supervisors"""
        self.client.force_login(self.superuser)
        res = self.client.get(self.detail_url)
        self.assertContains(res, 'Assign a member')

        self.client.force_login(self.supervisor)
        res = self.client.get(self.detail_url)
        self.assertContains(res, 'Assign a member')

        self.client.force_login(self.assigned)
        res = self.client.get(self.detail_url)
        self.assertNotContains(res, 'Assign a member')

        self.client.force_login(self.member)
        res = self.client.get(self.detail_url)
        self.assertNotContains(res, 'Assign a member')


class TestBugCreateView(TestCase):
    """Test the bug create view"""

    def setUp(self):
        self.member = utils.sample_member()
        self.project = utils.sample_project(creator=self.member)
        self.project.members.add(self.member)

        self.client = Client()
        self.client.force_login(self.member)
        self.create_url = reverse('bugs:create')

    def test_bug_create_view_GET_POST_PUT_only(self):
        """Test only GET, POST and PUT requests are allowed to create view"""
        res = self.client.patch(self.create_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.delete(self.create_url)
        self.assertEqual(res.status_code, 405)

    def test_bug_create_view_GET_basic_successful(self):
        """Test GETting create view with no optinal parameters"""
        res = self.client.get(self.create_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'bugs/create.html')
        self.assertContains(res, 'Title')
        self.assertContains(res, 'Description')
        self.assertContains(res, 'Project')

    def test_bug_create_view_GET_default_project_successful(self):
        """Test GETting create view with optinal parameters"""
        res = self.client.get(self.create_url + f'?project={self.project.id}')

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'bugs/create.html')
        self.assertContains(res, 'Title')
        self.assertContains(res, 'Description')
        self.assertContains(res, 'Project')

    def test_bug_create_view_POST_successful(self):
        """Test a bug is created when a valid request is made to create view"""
        res = self.client.post(self.create_url, {
            'title': 'Bug Title 123',
            'description': 'A bug description',
            'project': self.project.id
        })

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Bug.objects.filter(title='Bug Title 123').exists())

    def test_bug_create_view_sets_creator_and_date_automatically(self):
        """Test the bug creator and creation date are set automatically"""
        res = self.client.post(self.create_url, {
            'title': 'Bug Title 123',
            'description': 'A bug description',
            'project': self.project.id
        })

        self.assertEqual(res.status_code, 302)
        bug = Bug.objects.get(title='Bug Title 123')

        self.assertEqual(bug.creator, self.member)
        self.assertEqual(bug.creationDate.date(), datetime.date.today())

    def test_bug_create_view_missing_field(self):
        """Test a missing required field returns an error"""
        res = self.client.post(self.create_url, {
            'description': 'A bug description',
            'project': self.project.id
        })
        self.assertEqual(res.status_code, 200)
        self.assertFalse(
            Bug.objects.filter(description='A bug description').exists()
        )

        res = self.client.post(self.create_url, {
            'title': 'Bug Title 456',
            'description': 'A bug description',
        })
        self.assertEqual(res.status_code, 200)
        self.assertFalse(
            Bug.objects.filter(title='Bug Title 456').exists()
        )

    def test_bug_create_view_invalid_project(self):
        """Test an invalid project returns an error"""
        res = self.client.post(self.create_url, {
            'title': 'Bug Title 456',
            'description': 'A bug description',
            'project': 123
        })

        self.assertEqual(res.status_code, 200)
        self.assertFalse(
            Bug.objects.filter(title='Bug Title 456').exists()
        )


class TestBugUpdateView(TestCase):
    """Test the bug update view"""

    def setUp(self):
        self.member = utils.sample_member()
        self.project = utils.sample_project(creator=self.member)
        self.project.members.add(self.member)
        self.project.supervisors.add(self.member)
        self.bug = utils.sample_bug(creator=self.member, project=self.project)

        self.client = Client()
        self.client.force_login(self.member)
        self.update_url = reverse('bugs:update', args=[self.bug.id])

    def test_bug_update_view_no_DELETE(self):
        """Test DELETE requests are not allowed to update view"""
        res = self.client.delete(self.update_url)
        self.assertEqual(res.status_code, 405)

    def test_bug_update_view_GET(self):
        """Test GETting update view with no optinal parameters"""
        res = self.client.get(self.update_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'bugs/update.html')

        self.assertContains(res, 'Title')
        self.assertContains(res, self.bug.title)

        self.assertContains(res, 'Description')
        self.assertContains(res, self.bug.description)

    def test_bug_update_view_POST_successful(self):
        """Test a bug is updated when a valid request is made to update view"""
        res = self.client.post(self.update_url, {
            'title': 'Bug Title 123',
            'description': 'A bug description',
        })
        self.bug.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.bug.title, 'Bug Title 123')
        self.assertEqual(self.bug.description, 'A bug description')
