Django Comment System
=====================

Installation & Configuration
----------------------------

1. Install using pip

   .. code:: shell

      python -m pip install django-comment-system

   or Clone the repository and copy ``comment`` folder and paste in project folder.

   .. code:: shell

      git clone https://github.com/mahyar-amiri/django-comment-system.git


2. Add ``comment.apps.CommentConfig`` to installed_apps in the
   ``settings.py`` file after ``django.contrib.auth``.

   .. code:: python

      # setting.py

      INSTALLED_APPS = [
          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'django.contrib.staticfiles',

          # MY APPS
          'comment.apps.CommentConfig',
      ]
      LOGIN_URL = reverse_lazy('admin:login')  # or your account login url
      MEDIA_URL = '/media/'
      MEDIA_ROOT = BASE_DIR / 'media'

3. Add ``path('comment/', include('comment.urls')),`` to urlpatterns in
   the ``urls.py`` file.

   .. code:: python

      # urls.py

      from django.urls import path, include

      urlpatterns = [
           path('comment/', include('comment.urls')),
      ]
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


4. Connect ``comments`` to target model. In ``models.py`` add the field
   ``comments`` as a GenericRelation field to the required model.

   **NOTE:** Please note that the field name must be ``comments``
   **NOT** ``comment``.

   .. code:: python

      # models.py

      from django.db import models
      from django.contrib.contenttypes.fields import GenericRelation
      from comment.models import Comment

      class Article(models.Model):
          title = models.CharField(max_length=20)
          content = models.TextField()
          # the field name should be comments
          comments = GenericRelation(Comment)

5. Do migrations

   .. code:: shell

      python manage.py migrate

Usage
-----

1. In the template (e.g. post_detail.html) add the following template
   tags where obj is the instance of post model.

   .. code:: html

      {% load comment_tags %}

2. Add the following template tags where you want to render comments.

   .. code:: html

      {% render_comments request obj settings_slug='default-config' %}  {# Render all the comments belong to the passed object "obj" #}

   if your context_object_name is not ``obj`` (e.g article) replace obj
   with context_object_name.

   .. code:: html

      {% render_comments request obj=article settings_slug='default-config' %}
