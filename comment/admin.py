from django.contrib import admin, messages
from django.utils.translation import ngettext

from comment.models import Comment, React, Reaction


class ListFilterByParent(admin.SimpleListFilter):
    title = 'parent'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        return (
            ('parent', 'Comments'), ('child', 'Replies')
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'parent':
                return queryset.filter(parent__isnull=True)
            elif self.value() == 'child':
                return queryset.filter(parent__isnull=False)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'is_spoiler', 'status', 'content_object', 'posted')
    ordering = ('-posted',)
    search_fields = ('content',)
    list_filter = ('is_spoiler', 'status', ListFilterByParent)
    readonly_fields = ('content', 'user', 'parent', 'content_type', 'content_object', 'object_id', 'urlhash', 'posted')
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


class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'react')
    list_filter = ('react__emoji',)
    search_fields = ('user', 'comment')


class ReactAdmin(admin.ModelAdmin):
    list_display = ('slug', 'emoji', 'source_file')
    search_fields = ('slug', 'emoji')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Reaction, ReactionAdmin)
admin.site.register(React, ReactAdmin)
