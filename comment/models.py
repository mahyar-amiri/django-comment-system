from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html

from comment.managers import CommentQuerySet, ReactionQuerySet

User = get_user_model()


class CommentSettings(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(primary_key=True, help_text='This value will be used in render_comments tag')

    default_profile_image = models.ImageField(upload_to='comment_default_profile_images', null=True, blank=True)
    content_words_count = models.PositiveSmallIntegerField(default=40, help_text='More than this value will have Read More button in comment content')
    status_check = models.BooleanField(default=False, help_text='If True, comment status will be set as d(Delivered) otherwise it will be set as a(Accepted).')
    allow_spoiler = models.BooleanField(default=True)
    allow_reply = models.BooleanField(default=True)
    allow_edit = models.BooleanField(default=True)
    allow_delete = models.BooleanField(default=True)
    allow_reaction = models.BooleanField(default=True, help_text='First, create a react emoji in React models')
    reaction_type = models.CharField(max_length=6, choices=(('emoji', 'Emoji'), ('source', 'Source')), default='emoji', help_text='Add source in React model')
    per_page = models.PositiveSmallIntegerField(default=10, help_text='Set 0 if you don\'t want pagination (All comments will be shown at once)')
    time_type = models.PositiveSmallIntegerField(default=1, choices=((1, 'Compound'), (2, 'From Now'), (3, 'Date & Time')), help_text='Comment posted time style')
    time_days = models.PositiveSmallIntegerField(default=3, help_text='Less than this value will use FROM NOW type , more will use DATE & TIME type')
    theme_direction = models.CharField(max_length=3, choices=(('ltr', 'LTR (Left to Right)'), ('rtl', 'RTL (Right to Left)')), default='ltr')
    theme_dark_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Comment Settings'
        verbose_name_plural = 'Comment Settings'

    def __str__(self):
        return f'{self.name} - [{self.slug}]'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    is_spoiler = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    STATUS_CHOICES = (('d', 'Delivered'), ('a', 'Accepted'), ('r', 'Rejected'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    urlhash = models.CharField(max_length=50, unique=True, editable=False)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CommentQuerySet.as_manager()

    class Meta:
        ordering = ('-is_pinned', '-posted')

    def __str__(self):
        if not self.parent:
            return f'{self.content[:20]}'
        else:
            return f'[RE] ({self.parent.content[:10]}) : {self.content[:15]}'

    def set_unique_urlhash(self):
        if not self.urlhash:
            self.urlhash = self.__class__.objects.generate_urlhash()
            while self.__class__.objects.filter(urlhash=self.urlhash).exists():
                self.urlhash = self.__class__.objects.generate_urlhash()

    def save(self, *args, **kwargs):
        self.set_unique_urlhash()
        super(Comment, self).save(*args, **kwargs)

    def is_updated(self):
        return True if self.updated.timestamp() > self.posted.timestamp() else False

    is_updated.boolean = True

    @property
    def is_parent(self):
        return self.parent is None


class React(models.Model):
    slug = models.CharField(max_length=20, unique=True)
    emoji = models.CharField(max_length=5)
    source = models.ImageField(upload_to='react_source', null=True, blank=True)

    def __str__(self):
        return self.slug

    def source_file(self):
        return format_html(f"<img style='height:20px' src='{self.source.url}' alt='{self.emoji}'>") if self.source else 'X'


class Reaction(models.Model):
    user = models.ForeignKey(User, related_name='comment_reactions', on_delete=models.CASCADE, editable=False)
    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE, editable=False)
    react = models.ForeignKey(React, related_name='reactions', on_delete=models.CASCADE, editable=False)

    objects = ReactionQuerySet.as_manager()

    class Meta:
        unique_together = ['user', 'comment']

    def __str__(self):
        return f'{self.user} <{self.react.slug}> ({self.comment.content[:20]})'
