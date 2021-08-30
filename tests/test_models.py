from django.test import TestCase

from django.contrib.auth.models import User
from django_helpdesk import models

from datetime import datetime


class TicketTestCase(TestCase):
    def test_save_closed(self):
        author = User.objects.create(username='author')
        ticket = models.Ticket.objects.create(title='title', author=author)

        self.assertFalse(ticket.closed)
        self.assertIsNone(ticket.closed_on)

        now = datetime.now()
        ticket.closed = True
        ticket.save()

        self.assertTrue(ticket.closed)
        self.assertGreaterEqual(ticket.closed_on, now)

    def test_save_reopened(self):
        author = User.objects.create(username='author')
        ticket = models.Ticket.objects.create(title='title', author=author,
                                              closed=True)

        self.assertTrue(ticket.closed)

        ticket.closed = False
        ticket.save()

        self.assertFalse(ticket.closed)
        self.assertIsNone(ticket.closed_on)
