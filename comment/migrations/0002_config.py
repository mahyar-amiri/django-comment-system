import io
import os
import time

import requests
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import migrations


def save_image_from_url(url):
    response = requests.get(url)
    file = io.BytesIO(response.content)
    filename = os.path.basename(url)
    name, ext = os.path.splitext(filename)
    file_name = f'{name}-{time.time()}{ext}'
    uploaded_file = InMemoryUploadedFile(file, None, file_name, 'image/svg', file.getbuffer().nbytes, None)
    return uploaded_file, file_name


def InitialCommentSettings(apps, schema_editor):
    CommentSettings = apps.get_model('comment', 'CommentSettings')

    print('Fetching default_profile_image from web')

    # STAR RATING CONFIG
    file, file_name = save_image_from_url(url="https://raw.githubusercontent.com/mahyar-amiri/django-comment-system/master/comment/static/comment/img/profile.png")
    CommentSettings.objects.create(name='Default Config', slug='default-config', default_profile_image=File(file, file_name))


def InitialReact(apps, schema_editor):
    React = apps.get_model('comment', 'React')
    React.objects.create(slug='like', emoji='👍')
    React.objects.create(slug='dislike', emoji='👎')


class Migration(migrations.Migration):
    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(InitialCommentSettings),
        migrations.RunPython(InitialReact),
    ]
