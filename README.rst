Django Tailwind Comments
===============

Installation & Configuration
----------------------------

1. Clone the repository

   .. code::

      git clone https://github.com/lordmahyar/django-tailwind-comments.git

2. Copy ``comment`` folder and paste in project folder.

3. Add ``comment.apps.CommentConfig`` to installed_apps in the
   ``settings.py`` file after ``django.contrib.auth``.

   .. code::

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

4. Add ``path('comment/', include('comment.urls')),`` to urlpatterns in
   the ``urls.py`` file.

   .. code::

      # urls.py

      from django.urls import path, include

      urlpatterns = [
           path('comment/', include('comment.urls')),
      ]

5. Connect ``comments`` to target model. In ``models.py`` add the field
   ``comments`` as a GenericRelation field to the required model.

   **NOTE:** Please note that the field name must be ``comments``
   **NOT** ``comment``.

   .. code::

      # models.py

      from django.db import models
      from django.contrib.contenttypes.fields import GenericRelation
      from comment.models import Comment

      class Article(models.Model):
          title = models.CharField(max_length=20)
          content = models.TextField()
          # the field name should be comments
          comments = GenericRelation(Comment)

6. Do migrations

   .. code::

      python manage.py makemigrations
      python manage.py migrate

Usage
-----

1. In the template (e.g. post_detail.html) add the following template
   tags where obj is the instance of post model.

   .. code::

      {% load comment_tags %}

2. Add the following template tags where you want to render comments.

   .. code::

      {% render_comments request obj %}  {# Render all the comments belong to the passed object "obj" #}

   if your context_object_name is not ``obj`` (e.g. article) replace obj
   with context_object_name.

   .. code::

      {% render_comments request obj=article %}

Reactions
---------

1. Setup Reaction in ``settings.py``.

   .. code::

      # settings.py

      COMMENT_ALLOW_REACTION = True

2. Use admin panel to add react emoji. you will need an emoji and an
   emoji name as slug.

you can use image or gif instead of emoji character :
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3. In your admin panel, add image or gif file in React object.

4. Setup Reaction type in ``settings.py``.

   you have only 2 options : ``emoji`` or ``source``

   .. code::

      # settings.py

      COMMENT_REACTION_TYPE = 'source'  # emoji / source

Translation
-----------

1. Add ``locale`` folder to your app folder.

2. Run command below to create ``django.po`` file for your language.

   Find your language code
   `here <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`__.

   .. code::

      python manage.py makemessages -l MY_LANGUAGE_CODE
      # for generating translations corresponding to javascript code
      python manage.py makemessages -l MY_LANGUAGE_CODE -d djangojs

   e.g. The persian language code is ``fa``.

   .. code::

      python manage.py makemessages -l fa
      python manage.py makemessages -l fa -d djangojs

   This will create two ``.po`` files inside the
   ``locale/{MY_LANGUAGE_CODE}/LC_MESSAGES/`` directory.

3. After adding translation to both files, run the following command to
   verify everything is working.

   .. code::

      python manage.py compilemessages -l MY_LANGUAGE_CODE
      # e.g. for persian translation use fa instead of MY_LANGUAGE_CODE

   If you don’t see an error in the last command, your translations have
   been added in the correct format.

4. In ``settings.py`` to enable internationalization in your django
   applications.

   .. code::

      # settings.py

      USE_I18N = True
      USE_L18N = True
      LANGUAGE_CODE = '{MY_LANGUAGE_CODE}'  # 'en-us' for english , 'fa-ir' for persian , ...

Settings
--------

You can customize settings by adding keywords in ``settings.py``.

.. code::

   # setting.py

   # generated urlhash length
   COMMENT_URLHASH_LENGTH = 8

   # the comments need to be set as a(Accepted) to be shown in the comments list.
   # if True, comment status will be set as d(Delivered) otherwise it will be set as a(Accepted).
   COMMENT_STATUS_CHECK = False

   # if True, tailwindcss and jquery package will be loaded from static files.
   COMMENT_OFFLINE_IMPORTS = True

   # if None, comments will be shown without profile image
   # you should set this value as profile image field name
   # for example our abstract user profile picture field is profile_image
   # <img src="{{ user.profile_image.url }}" /> so we set COMMENT_PROFILE_IMAGE_FIELD = 'profile.image'
   # see link blew to create abstract user model
   # https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model
   COMMENT_PROFILE_IMAGE_FIELD = None
   # default profile image static path
   COMMENT_PROFILE_IMAGE_DEFAULT = 'img/profile.png'

   # activate spoiler comment mode 
   COMMENT_ALLOW_SPOILER = True
   # let users reply to a comment  
   COMMENT_ALLOW_REPLY = True
   # let users edit their comment  
   COMMENT_ALLOW_EDIT = True
   # let users delete their comment  
   COMMENT_ALLOW_DELETE = True

   # more than this value will have Read More button in comment content
   COMMENT_CONTENT_WORDS_COUNT = 40

   # let users react to a comment  
   COMMENT_ALLOW_REACTION = False
   # get emoji or from file source  
   COMMENT_REACTION_TYPE = 'emoji'  # emoji / source

   # number of comments per page
   # set 0 if you don't want pagination
   COMMENT_PER_PAGE = 10

   COMMENT_TIME_TYPE = 1  # 1.both 2.from_now 3.date_time
   COMMENT_TIME_DAYS = 3  # less will use type 2 , more will use type 3

   # set direction of comment section
   COMMENT_THEME_DIRECTION = 'ltr'  # ltr / rtl
   # set True for dark mode
   COMMENT_THEME_DARK_MODE = False

Front-End
---------

.. raw:: html

   <details>

.. raw:: html

   <summary>

Templates Folder Tree

.. raw:: html

   </summary>

.. raw:: html

   <p>

.. code::

   templates
      +-- comment
        --- comments.html
        --- comment_list.html
        --- comment_counter.html
        --- comment_body.html
        --- comment_reactions.html
        --- object_info.html
      +-- forms
        --- comment_form_create.html
        --- comment_form_reply.html
        --- comment_form_edit.html
        --- comment_form_delete.html
      +-- icons
        --- icon_arrow_backward.html
        --- icon_arrow_forward.html
        --- icon_delete.html
        --- icon_dots.html
        --- icon_down.html
        --- icon_edit.html
        --- icon_eye.html
        --- icon_eye_off.html
        --- icon_up.html
      +-- utils
        --- comment_list_pagination.html
        --- comment_list_loader.html
        --- comment_list_empty.html
        --- IMPORTS.html
        --- SCRIPTS.html

.. raw:: html

   </p>

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

Static Folder Tree

.. raw:: html

   </summary>

.. raw:: html

   <p>

.. code::

   static
      +-- css
        --- style.css
        --- style.min.css
      +-- img
        --- profile.png
      +-- js
        --- comment.js
        --- comment.min.js
        --- jquery.min.js

.. raw:: html

   </p>

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

IDs

.. raw:: html

   </summary>

.. raw:: html

   <p>

.. code::

   #comments
      --- #comment-modal
      --- #comment-list
      --- #comment-react-list
      --- #comment-{urlhash}
      +-- forms
        --- #form-comment-create
        --- #form-comment-edit-{urlhash}
        --- #form-comment-delete-{urlhash}
        --- #form-comment-reply-{urlhash}
        --- #form-comment-react-{urlhash}
      +-- toggles
        --- #toggle-spoiler-{urlhash}
        --- #toggle-edit-{urlhash}
        --- #toggle-reply-{urlhash}
        --- #toggle-more-{urlhash}

.. raw:: html

   </p>

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

Handle 403 ERROR Template Page

.. raw:: html

   </summary>

.. raw:: html

   <p>

1. Create ``403.html`` in your template path.

2. Add custom view in ``views.py``.

   .. code::

      # views.py
      from django.shortcuts import render
      def custom_error_403(request, exception):
          return render(request, '403.html', {'exception': exception})

3. Add handler403 in your project ``urls.py``

   .. code::

      # urls.py
      handler403 = 'my_project.views.custom_error_403'

.. raw:: html

   </p>

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

Minify Static Files

.. raw:: html

   </summary>

.. raw:: html

   <p>

1. Installation

   .. code::

      npm i minify -g

2. Usage

   .. code::

      npm static/css/style.css > static/css/style.min.css
      npm static/js/comment.js > static/js/comment.min.js

.. raw:: html

   </p>

.. raw:: html

   </details>
