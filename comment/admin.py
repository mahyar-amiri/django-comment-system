from django.contrib import admin, messages
from django.utils.translation import ngettext

from comment.models import Comment, React, Reaction, CommentSettings


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


class ListFilterByUpdated(admin.SimpleListFilter):
    title = 'is updated'
    parameter_name = 'is_updated'

    def lookups(self, request, model_admin):
        return (
            ('updated', 'Yes'), ('not_updated', 'No')
        )

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'updated':
                return queryset.filter_updated()
            elif self.value() == 'not_updated':
                return queryset.filter_not_updated()


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'is_spoiler', 'is_pinned', 'is_updated', 'status', 'content_object', 'posted')
    ordering = ('-is_pinned', '-posted',)
    search_fields = ('content',)
    list_filter = ('is_spoiler', 'is_pinned', ListFilterByUpdated, 'status', ListFilterByParent)
    readonly_fields = ('user', 'content', 'parent', 'content_type', 'content_object', 'object_id', 'urlhash', 'posted', 'is_spoiler', 'is_pinned', 'status')
    actions = ['accept_comment', 'reject_comment', 'pin_comment', 'unpin_comment', 'set_spoiler_comment', 'unset_spoiler_comment']

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

    def pin_comment(self, request, queryset):
        pinned = queryset.update(is_pinned=True)
        self.message_user(request,
                          ngettext(f'{pinned} comment pinned.',
                                   f'{pinned} comments pinned.', pinned),
                          messages.SUCCESS)

    pin_comment.short_description = 'Pin selected comments'

    def unpin_comment(self, request, queryset):
        unpinned = queryset.update(is_pinned=False)
        self.message_user(request,
                          ngettext(f'{unpinned} comment unpinned.',
                                   f'{unpinned} comments unpinned.', unpinned),
                          messages.SUCCESS)

    unpin_comment.short_description = 'Unpin selected comments'

    def set_spoiler_comment(self, request, queryset):
        spoiler = queryset.update(is_spoiler=True)
        self.message_user(request,
                          ngettext(f'{spoiler} comment set as spoiler.',
                                   f'{spoiler} comments set as spoiler.', spoiler),
                          messages.SUCCESS)

    set_spoiler_comment.short_description = 'Set selected comments as spoiler'

    def unset_spoiler_comment(self, request, queryset):
        spoiler = queryset.update(is_spoiler=False)
        self.message_user(request,
                          ngettext(f'{spoiler} comment unset as spoiler.',
                                   f'{spoiler} comments unset as spoiler.', spoiler),
                          messages.SUCCESS)

    unset_spoiler_comment.short_description = 'Unset selected comments as spoiler'


class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'react')
    list_filter = ('react__emoji',)
    search_fields = ('user', 'comment')
    readonly_fields = ('user', 'comment', 'react')


class ReactAdmin(admin.ModelAdmin):
    list_display = ('slug', 'emoji', 'source_file')
    search_fields = ('slug', 'emoji')


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(CommentSettings, SettingsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reaction, ReactionAdmin)
admin.site.register(React, ReactAdmin)
