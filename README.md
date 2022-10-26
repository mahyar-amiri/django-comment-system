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

## Templates Tree

```bash
comment
   └── templates
           ├── comments
           │   ├── comment_form.html
           │   ├── comments.html
           │   ├── comment_lis.html
           │   └── object_info.html
           └── IMPORTS.html
```

## Handle 403 ERROR Template Page

1. Create `403.html` in your template path.
2. Add custom view in `views.py`.
   ```python
   from django.shortcuts import render
   def custom_error_403(request, exception):
       return render(request, '403.html', {'exception': exception})
   ```
3. Add handler403 in your project `urls.py`
   ```python
   handler403 = 'my_project.views.custom_error_403'
   ```
