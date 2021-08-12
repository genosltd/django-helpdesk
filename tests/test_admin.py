from django.test import TestCase, RequestFactory
# from django.test import Client
from django.urls import reverse

from django.contrib.auth.models import User, Permission
from django.contrib import admin

from django_helpdesk import models
from django_helpdesk.admin import TicketAdmin


class TicketAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            username='author',
            password='password',
            is_staff=True
        )
        cls.user = User.objects.create(
            username='user',
            password='password',
            is_staff=True
        )
        cls.admin = User.objects.create(
            username='admin',
            password='password',
            is_staff=True,
            is_superuser=True
        )
        cls.ticket = models.Ticket.objects.create(title='title',
                                                  author=cls.author)
        cls.ticket_admin = TicketAdmin(models.Ticket, admin.site)
        cls.request_factory = RequestFactory()
        cls.ticket_change_request = cls.request_factory.get(
            reverse('admin:django_helpdesk_ticket_change',
                    args=(cls.ticket.id,))
        )

    def test_get_readonly_fields_for_author(self):
        self.ticket_change_request.user = self.author

        readonly_fields = self.ticket_admin.get_readonly_fields(
            self.ticket_change_request,
            self.ticket
        )
        self.assertIn('assigned_to', readonly_fields)
        self.assertNotIn('closed', readonly_fields)

    def test_get_readonly_fields_for_new_ticket(self):
        ticket_add_request = self.request_factory.get(
            reverse('admin:django_helpdesk_ticket_add')
        )
        ticket_add_request.user = self.user

        readonly_fields = self.ticket_admin.get_readonly_fields(
            ticket_add_request
        )
        self.assertIn('assigned_to', readonly_fields)
        self.assertIn('closed', readonly_fields)

    def test_get_readonly_fields_for_user(self):
        self.ticket_change_request.user = self.user

        readonly_fields = self.ticket_admin.get_readonly_fields(
            self.ticket_change_request,
            self.ticket
        )
        self.assertIn('assigned_to', readonly_fields)
        self.assertIn('closed', readonly_fields)

    def test_get_readonly_fields_for_user_with_assign_permission(self):
        can_assign_ticket = Permission.objects.get(
            codename='can_assign_ticket'
        )
        user = User.objects.create(
            username='user_with_perm',
            password='password',
            is_staff=True
        )
        user.user_permissions.add(can_assign_ticket)
        user = User.objects.get(pk=user.id)
        self.ticket_change_request.user = user

        readonly_fields = self.ticket_admin.get_readonly_fields(
            self.ticket_change_request,
            self.ticket
        )
        self.assertNotIn('assigned_to', readonly_fields)
        self.assertIn('closed', readonly_fields)

    def test_has_change_permission_for_model_in_general(self):
        admin = self.admin
        ticket_change_request = self.ticket_change_request
        ticket_change_request.user = admin

        change_permission = self.ticket_admin.has_change_permission(
            ticket_change_request
        )
        self.assertTrue(change_permission)

    def test_has_change_permission_for_admin(self):
        admin = self.admin
        ticket_change_request = self.ticket_change_request
        ticket_change_request.user = admin

        change_permission = self.ticket_admin.has_change_permission(
            ticket_change_request,
            self.ticket
        )
        self.assertTrue(change_permission)

    def test_has_change_permission_for_author(self):
        author = self.author
        ticket_change_request = self.ticket_change_request

        permissions = Permission.objects.filter(codename__icontains='ticket')
        author.user_permissions.set(permissions)
        author = User.objects.get(pk=author.id)

        ticket_change_request.user = author

        change_permission = self.ticket_admin.has_change_permission(
            ticket_change_request,
            self.ticket
        )
        self.assertTrue(change_permission)

    def test_has_change_permission_for_user(self):
        user = self.user
        ticket_change_request = self.ticket_change_request
        ticket_change_request.user = user

        change_permission = self.ticket_admin.has_change_permission(
            ticket_change_request,
            self.ticket
        )
        self.assertFalse(change_permission)

    def test_save_model(self):
        client = self.client
        client.force_login(user=self.admin)
        response = client.post(reverse('admin:django_helpdesk_ticket_add'), {
            'title': 'test_save_model'
        }, follow=True)

        new_ticket = models.Ticket.objects.get(title='test_save_model')
        self.assertEqual(new_ticket.author, self.admin)

