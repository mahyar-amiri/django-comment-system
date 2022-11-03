from django.urls import path
from comment import views

app_name = 'comment'
urlpatterns = [
    path('list/', views.CommentList.as_view(), name='list'),
    path('create/', views.CommentCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.CommentUpdate.as_view(), name='update'),
    path('delete/<str:urlhash>/', views.CommentDelete.as_view(), name='delete'),
]
