# Django Comments

## Installation & Configuration

1. Clone the repository

   ```shell
   git clone https://github.com/lordmahyar/django-comments.git
   ```

2. Copy `comment` folder and paste in project folder.
3. Add `comment.apps.CommentConfig` to installed_apps in the `settings.py` file after `django.contrib.auth`.

   ```python
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
   ```

4. Add `path('comment/', include('comment.urls')),` to urlpatterns in the `urls.py` file.

   ```python
   # urls.py

   from django.urls import path, include

   urlpatterns = [
        path('comment/', include('comment.urls')),
   ]
   ```

5. Connect `comments` to target model. In `models.py` add the field `comments` as a GenericRelation field to the
   required model.

   **NOTE:** Please note that the field name must be `comments` **NOT** `comment`.

   ```python
   # models.py
   
   from django.db import models
   from django.contrib.contenttypes.fields import GenericRelation
   from comment.models import Comment
   
   class Article(models.Model):
       title = models.CharField(max_length=20)
       content = models.TextField()
       # the field name should be comments
       comments = GenericRelation(Comment)

   ```

6. Do migrations
   ```shell
   python manage.py makemigrations
   python manage.py migrate
   ```

## Usage

1. In the template (e.g. post_detail.html) add the following template tags where obj is the instance of post model.
   ```html
   {% load comment_tags %}
   ```

2. Add the following template tags where you want to render comments.
   ```html
   {% render_comments request obj %}  {# Render all the comments belong to the passed object "obj" #}
   ```
   if your context_object_name is not `obj` (e.g. article) replace obj with context_object_name.
   ```html
   {% render_comments request obj=article %}
   ```

## Settings

You can customize settings by adding keywords in `settings.py`.

```python
# setting.py

# generated urlhash length
COMMENT_URLHASH_LENGTH = 8

# the comments need to be set as a(Accepted) to be shown in the comments list.
# if True comment status will be set as d(Delivered) otherwise it will be set as a(Accepted).
COMMENT_STATUS_CHECK = False

# if true, tailwindcss and jquery package will be loaded from static files.
COMMENT_OFFLINE_IMPORTS = True

# if None comments will be shown without profile image
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
# let users reply to comment  
COMMENT_ALLOW_REPLY = True
# let users edit their comment  
COMMENT_ALLOW_EDIT = True
# let users delete their comment  
COMMENT_ALLOW_DELETE = True

# more than this value will have Read More button in comment content
COMMENT_CONTENT_WORDS_COUNT = 40
```

## Front-End

### Templates Folder Tree

```text
templates
   ├── comment
   │    ├── comments.html
   │    ├── comment_list.html
   │    ├── comment_counter.html
   │    ├── comment_body.html
   │    └── object_info.html
   │
   ├── forms
   │    ├── comment_form_create.html
   │    ├── comment_form_reply.html
   │    ├── comment_form_edit.html
   │    └── comment_form_delete.html
   │
   ├── icons
   │    ├── icon_dots.html
   │    ├── icon_edit.html
   │    ├── icon_delete.html
   │    ├── icon_eye.html
   │    └── icon_eye_off.html
   │
   └── utils
        ├── comment_list_empty.html
        ├── comment_list_loader.html
        ├── IMPORTS.html
        └── SCRIPTS.html
```

### Static Folder Tree

```text
static
   ├── css
   │    └── style.css
   ├── img
   │    └── profile.png
   └── js
        ├── comment.js
        └── jquery.min.js
```

### IDs

```text
#comments
   ├── #comment-modal
   ├── #comment-list
   │
   ├── #comment-{urlhash}
   │
   ├── forms
   │    ├── #form-comment-create
   │    ├── #form-comment-edit-{urlhash}
   │    ├── #form-comment-delete-{urlhash}
   │    └── #form-comment-reply-{urlhash}
   │
   └── toggles
        ├── #toggle-spoiler-{urlhash}
        ├── #toggle-edit-{urlhash}
        └── #toggle-reply-{urlhash}
```

## Handle 403 ERROR Template Page

1. Create `403.html` in your template path.
2. Add custom view in `views.py`.
   ```python
   # views.py
   from django.shortcuts import render
   def custom_error_403(request, exception):
       return render(request, '403.html', {'exception': exception})
   ```
3. Add handler403 in your project `urls.py`
   ```python
   # urls.py
   handler403 = 'my_project.views.custom_error_403'
   ```
