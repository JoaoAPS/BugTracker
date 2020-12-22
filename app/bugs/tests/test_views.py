import datetime

from django.test import TestCase, Client
from django.urls import reverse

from core import utils
from bugs.models import Bug, Message


class TestBugViewsPermissions(TestCase):
    """Test the bug views permission"""

    def setUp(self):
        self.client = Client()

        self.member = utils.sample_member()
        self.creator = utils.sample_member(email="other@mail.com")
        self.superuser = utils.sample_superuser()
        self.project = utils.sample_project()
        self.project.members.add(self.creator)
        self.bug = utils.sample_bug(creator=self.creator, project=self.project)

        self.list_url = reverse('bugs:list')
        self.detail_url = reverse('bugs:detail', args=[self.bug.id])
        self.create_url = reverse('bugs:create')
        self.update_url = reverse('bugs:update', args=[self.bug.id])
        self.creator_update_url = reverse(
            'bugs:creator_update', args=[self.bug.id]
        )
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
            self.creator_update_url,
        ]:
            res = self.client.get(url)
            redirect_url = res.url.split('?')[0]

            self.assertEqual(res.status_code, 302)
            self.assertEqual(redirect_url, reverse('members:login'))

        for url in [
            self.create_url,
            self.update_url,
            self.creator_update_url,
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
            self.creator_update_url,
        ]:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200)

        for url in [
            self.create_url,
            self.update_url,
            self.creator_update_url,
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

        res = self.client.get(self.creator_update_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.create_url)
        self.assertNotIn(res.status_code, [404, 403, 302])

        res = self.client.post(self.update_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.creator_update_url)
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

        res = self.client.get(self.creator_update_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.create_url, self.bugPayload)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.update_url)
        self.assertEqual(res.status_code, 403)

        res = self.client.post(self.creator_update_url)
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

    def test_bug_detail_messages(self):
        """Test the bug messages are correctly passed to context"""
        self.client.force_login(self.member)
        other_bug = utils.sample_bug(
            creator=self.supervisor, project=self.project
        )

        Message.objects.create(
            content="Mess 5", bug=self.bug, writer=self.member
        )
        Message.objects.create(
            content="Mess 2", bug=self.bug, writer=self.member
        )
        Message.objects.create(
            content="Mess 1", bug=self.bug, writer=self.superuser
        )
        Message.objects.create(
            content="Mess 4", bug=self.bug, writer=self.supervisor
        )
        Message.objects.create(
            content="Mess 14", bug=other_bug, writer=self.member
        )
        Message.objects.create(
            content="Mess 13", bug=other_bug, writer=self.member
        )
        messages = Message.objects\
            .filter(bug=self.bug).order_by('-creationDate')

        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context['messages']), list(messages))


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


class TestBugCreatorUpdateView(TestCase):
    """Test the bug creator_update view"""

    def setUp(self):
        self.creator = utils.sample_member()
        self.project = utils.sample_project()
        self.project.members.add(self.creator)
        self.bug = utils.sample_bug(creator=self.creator, project=self.project)

        self.client = Client()
        self.client.force_login(self.creator)
        self.update_url = reverse('bugs:creator_update', args=[self.bug.id])

    def test_bug_creator_update_view_creator_allowed(self):
        """Test the bug creator can access the creator_update view"""
        res = self.client.get(self.update_url)
        self.assertEqual(res.status_code, 200)

        res = self.client.post(self.update_url)
        self.assertNotEqual(res.status_code, 403)

    def test_bug_creator_update_view_no_DELETE(self):
        """Test DELETE requests are not allowed to update view"""
        res = self.client.delete(self.update_url)
        self.assertEqual(res.status_code, 405)

    def test_bug_creator_update_view_GET(self):
        """Test GETting update view with no optinal parameters"""
        res = self.client.get(self.update_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'bugs/creator_update.html')

        self.assertContains(res, 'Title')
        self.assertContains(res, self.bug.title)

        self.assertContains(res, 'Description')
        self.assertContains(res, self.bug.description)

    def test_bug_creator_update_view_POST_successful(self):
        """Test a bug is updated when a valid request is made to update view"""
        res = self.client.post(self.update_url, {
            'title': 'Bug Title 123',
            'description': 'A bug description',
        })
        self.bug.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.bug.title, 'Bug Title 123')
        self.assertEqual(self.bug.description, 'A bug description')


class TestBugAssignMemberView(TestCase):
    """Test the bug AssignMember view"""

    def setUp(self):
        self.member = utils.sample_member(email='email1@mail.com')
        self.supervisor = utils.sample_member(email='email2@mail.com')
        self.project = utils.sample_project()
        self.project.members.add(self.member)
        self.project.members.add(self.supervisor)
        self.project.supervisors.add(self.supervisor)
        self.bug = utils.sample_bug(creator=self.member, project=self.project)

        self.client = Client()
        self.client.force_login(self.supervisor)

        self.assign_member_url = reverse(
            'bugs:assign_member', args=[self.bug.id]
        )

    def test_bug_assign_member_view_POST_only(self):
        """Test the bug 'assign_member' view only accepts POST requests"""
        res = self.client.get(self.assign_member_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.patch(self.assign_member_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.put(self.assign_member_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.delete(self.assign_member_url)
        self.assertEqual(res.status_code, 405)

    def test_bug_assign_member_view_succeful(self):
        """Test the bug 'assign_member' can successfully assign member"""
        m1 = utils.sample_member(email='email3@mail.com')
        m2 = utils.sample_member(email='email4@mail.com')

        self.project.members.add(m1)
        self.project.members.add(m2)

        res1 = self.client.post(
            self.assign_member_url, {'member_ids': [str(self.member.id)]}
        )
        res2 = self.client.post(
            self.assign_member_url, {'member_ids': [m1.id, m2.id]}
        )

        self.assertEqual(res1.status_code, 302)
        self.assertEqual(res2.status_code, 302)
        self.assertIn(self.member, self.bug.assigned_members.all())
        self.assertIn(m1, self.bug.assigned_members.all())
        self.assertIn(m2, self.bug.assigned_members.all())

    def test_bug_assign_member_view_errors(self):
        """Test the bug 'assign_member' view raises errors when needed"""
        non_project_member = utils.sample_member(email='nproject@mail.com')

        res = self.client.post(self.assign_member_url)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(self.bug.assigned_members.exists())

        res = self.client.post(self.assign_member_url, {'member_ids': 1})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(self.bug.assigned_members.exists())

        res = self.client.post(self.assign_member_url, {'member_ids': [2165]})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(self.bug.assigned_members.exists())

        res = self.client.post(
            self.assign_member_url, {'member_ids': non_project_member.id}
        )
        self.assertEqual(res.status_code, 400)
        self.assertFalse(self.bug.assigned_members.exists())


class TestBugChangeStatusView(TestCase):
    """Test the bug ChangeStatus view"""

    def setUp(self):
        self.supervisor = utils.sample_member(email='email2@mail.com')
        self.project = utils.sample_project()
        self.project.members.add(self.supervisor)
        self.project.supervisors.add(self.supervisor)
        self.bug = utils.sample_bug(
            creator=self.supervisor, project=self.project
        )
        self.bug.set_status(self.bug.WAITING_STATUS)

        self.client = Client()
        self.client.force_login(self.supervisor)

        self.change_status_url = reverse(
            'bugs:change_status', args=[self.bug.id]
        )

    def test_bug_change_status_view_POST_only(self):
        """Test the bug 'change_status' view accepts only POST requests"""
        res = self.client.get(self.change_status_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.patch(self.change_status_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.put(self.change_status_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.delete(self.change_status_url)
        self.assertEqual(res.status_code, 405)

    def test_bug_change_status_view_successful(self):
        """Test the bug 'change_status' view succesfully changes bug status"""
        res = self.client.post(self.change_status_url, {'status': 'FIXED'})
        self.bug.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.bug.status, 'FIXED')
        self.assertEqual(self.bug.closingDate.date(), datetime.date.today())

    def test_bug_change_status_view_error(self):
        """Test the bug 'change_status' view raises errors when needed"""
        res = self.client.post(self.change_status_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.bug.status, self.bug.WAITING_STATUS)

        res = self.client.post(
            self.change_status_url, {'status': 'nonexistent_status'}
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.bug.status, self.bug.WAITING_STATUS)

        res = self.client.post(self.change_status_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.bug.status, self.bug.WAITING_STATUS)

        res = self.client.post(self.change_status_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.bug.status, self.bug.WAITING_STATUS)


class TestBugChangeWorkingStatusView(TestCase):
    """Test the bug ChangeWorkingStatus view"""

    def setUp(self):
        self.supervisor = utils.sample_member(email='email2@mail.com')
        self.project = utils.sample_project()
        self.project.members.add(self.supervisor)
        self.project.supervisors.add(self.supervisor)
        self.bug = utils.sample_bug(
            creator=self.supervisor, project=self.project
        )
        self.bug.set_status(self.bug.WAITING_STATUS)

        self.client = Client()
        self.client.force_login(self.supervisor)

        self.change_working_status_url = reverse(
            'bugs:change_working_status', args=[self.bug.id]
        )

    def test_bug_change_working_status_view_POST_only(self):
        """Test bug 'change_working_status' view accepts only POST requests"""
        res = self.client.get(self.change_working_status_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.patch(self.change_working_status_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.put(self.change_working_status_url)
        self.assertEqual(res.status_code, 405)

        res = self.client.delete(self.change_working_status_url)
        self.assertEqual(res.status_code, 405)

    def test_bug_change_working_status_view_successful(self):
        """Test bug 'change_working_status' view succesfully changes status"""
        res = self.client.post(self.change_working_status_url, {'starting': 1})
        self.bug.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.bug.status, self.bug.WORKING_STATUS)

        res = self.client.post(self.change_working_status_url, {'starting': 0})
        self.bug.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.bug.status, self.bug.WAITING_STATUS)

    def test_bug_change_working_status_view_error(self):
        """Test bug 'change_working_status' view raises errors when needed"""
        res = self.client.post(self.change_working_status_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.bug.status, self.bug.WAITING_STATUS)

        res = self.client.post(
            self.change_working_status_url, {'starting': 'wrong'}
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(self.bug.status, self.bug.WAITING_STATUS)


class TestMessageViews(TestCase):
    """Test the views involving bug messages"""

    def setUp(self):
        self.superuser = utils.sample_superuser()
        self.supervisor = utils.sample_member(email="visor@mail.com")
        self.member = utils.sample_member()
        self.non_member = utils.sample_member(email="oither@mail.com")
        self.project = utils.sample_project(creator=self.supervisor)
        self.project.members.add(self.member)
        self.project.members.add(self.supervisor)
        self.project.supervisors.add(self.supervisor)
        self.bug = utils.sample_bug(
            creator=self.superuser, project=self.project
        )

        self.client = Client()
        self.message_create_url = reverse(
            'bugs:create_message', args=[self.bug.id]
        )

    def test_message_create_view_only_POST_allowed(self):
        """Test the message create view only accepts POST requests"""
        self.client.force_login(self.superuser)

        res = self.client.post(self.message_create_url)
        self.assertNotEqual(res.status_code, 405)

        for method in ['get', 'put', 'patch', 'delete']:
            res = getattr(self.client, method)(self.message_create_url)
            self.assertEqual(res.status_code, 405)

    def test_message_create_view_permissions(self):
        """Test the permission for the create_message view are correct"""
        res = self.client.post(self.message_create_url)
        self.assertRedirects(
            res,
            reverse('members:login') +
                f'?next=/bugs/{self.bug.id}/create_message'
        )

        self.client.force_login(self.non_member)
        res = self.client.post(self.message_create_url)
        self.assertEqual(res.status_code, 403)

        self.client.force_login(self.member)
        res = self.client.post(self.message_create_url)
        self.assertNotEqual(res.status_code, 403)

        self.client.force_login(self.supervisor)
        res = self.client.post(self.message_create_url)
        self.assertNotEqual(res.status_code, 403)

        self.client.force_login(self.superuser)
        res = self.client.post(self.message_create_url)
        self.assertNotEqual(res.status_code, 403)

    def test_message_create_view_successful(self):
        """Test the message create view automatically sets fields correctly"""
        payload = {'content': 'Test Message'}
        self.client.force_login(self.member)
        res = self.client.post(self.message_create_url, payload)
        message = Message.objects.filter(content=payload['content'])

        self.assertEqual(res.status_code, 302)
        self.assertTrue(message.exists())
        self.assertEqual(message[0].bug, self.bug)
        self.assertEqual(message[0].writer, self.member)
        self.assertEqual(message[0].creationDate.date(), datetime.date.today())

    def test_message_create_view_invalid_payload(self):
        """Test the message create view correctly handles invalid payloads"""
        self.client.force_login(self.member)

        res = self.client.post(self.message_create_url)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(Message.objects.exists())

        res = self.client.post(self.message_create_url, {'content': ''})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(Message.objects.exists())
