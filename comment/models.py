from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from comment import settings
from random import choice
from string import ascii_lowercase

User = get_user_model()


class CommentQuerySet(models.QuerySet):
    def filter_accepted(self):
        return self.filter(status='a')

    def filter_parents(self):
        return self.filter(parent__isnull=True)

    def order_newest(self):
        return self.order_by('-posted')

    def order_oldest(self):
        return self.order_by('posted')

    @staticmethod
    def generate_urlhash():
        return ''.join(choice(ascii_lowercase) for _ in range(settings.COMMENT_URLHASH_LENGTH))


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    is_spoiler = models.BooleanField(default=False)
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
        ordering = ('-posted',)

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
