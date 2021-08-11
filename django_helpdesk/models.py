from django.db import models
from django.conf import settings


class Ticket(models.Model):
    class Meta:
        permissions = (
            ('can_assign_ticket', 'Can assign ticket'),
        )
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='+',
                               editable=False)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE, related_name='+',
                                    blank=True, null=True)

    opened_on = models.DateTimeField(auto_now_add=True)

    closed = models.BooleanField(default=False)
    closed_on = models.DateTimeField(editable=False, null=True)
