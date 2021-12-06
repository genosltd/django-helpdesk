from django.contrib import admin

from django_hashtag.admin import HasHashtagsAdmin
from django_comment.admin import HasCommentsAdmin

from . import models


@admin.register(models.Ticket)
class TicketAdmin(HasHashtagsAdmin, HasCommentsAdmin):
    list_display = ('title', 'author', 'assigned_to', 'opened_on', 'closed_on')
    list_filter = ('author', 'assigned_to', 'opened_on', 'closed', 'closed_on')
    search_fields = (
        'author__username',
        'author__first_name',
        'author__last_name',
        'assigned_to__username',
        'assigned_to__first_name',
        'assigned_to__last_name',
        'title',
        'description',

        'comments__comment',
    )

    fields = ('author', 'title', 'description', 'assigned_to', 'opened_on',
              'closed', 'closed_on')
    readonly_fields = ('author', 'opened_on', 'closed_on')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = set(super().get_readonly_fields(request, obj=obj))
        user = request.user
        if obj is None:
            readonly_fields.add('closed')

        elif not user.is_superuser:
            if user not in set((obj.author, obj.assigned_to)):
                readonly_fields.add('closed')

        if not user.has_perm('django_helpdesk.can_assign_ticket'):
            readonly_fields.add('assigned_to')

        return tuple(readonly_fields)

    def has_change_permission(self, request, obj=None):
        change_permission = super().has_change_permission(request, obj=obj)
        if obj is None:
            return change_permission
        elif request.user.is_superuser:
            return change_permission
        elif request.user in set((obj.author, obj.assigned_to)):
            return change_permission
        else:
            return False

    has_delete_permission = has_change_permission

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
