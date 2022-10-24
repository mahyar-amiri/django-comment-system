from django.urls import path
from comment import views

app_name = 'comment'
urlpatterns = [
    path('create/', views.CreateComment.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdateComment.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteComment.as_view(), name='delete'),
]
