from django.urls import path
from comment.views import create_view

app_name = 'comment'
urlpatterns = [
    path('create/', create_view.as_view(), name='create'),
]
