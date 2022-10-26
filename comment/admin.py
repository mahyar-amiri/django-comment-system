from django.utils.translation import ngettext
from django.contrib import admin, messages
from comment.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'is_spoiler', 'status', 'content_object', 'posted')
    ordering = ('-posted',)
    search_fields = ('content',)
    list_filter = ('is_spoiler', 'status')
    readonly_fields = ('content', 'user', 'parent', 'content_object', 'content_type', 'object_id')
    list_editable = ('is_spoiler', 'status')
    actions = ['accept_comment', 'reject_comment']

    def accept_comment(self, request, queryset):
        accepted = queryset.update(status='a')
        self.message_user(request,
                          ngettext(f'{accepted} comment accepted.',
                                   f'{accepted} comments accepted.', accepted),
                          messages.SUCCESS)

    accept_comment.short_description = 'Accept selected comments'

    def reject_comment(self, request, queryset):
        rejected = queryset.update(status='r')
        self.message_user(request,
                          ngettext(f'{rejected} comment rejected.',
                                   f'{rejected} comments rejected.', rejected),
                          messages.WARNING)

    reject_comment.short_description = 'Reject selected comments'


admin.site.register(Comment, CommentAdmin)
