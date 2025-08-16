from django.urls import path
from . import views

urlpatterns = [
    path('comments/<int:pk>/article/', views.comment_article, name='comment_article'),
    path('like/<int:pk>/article/', views.like_article, name='like_article'),
    path('dislike/<int:pk>/article/', views.dislike_article, name='dislike_article'),
    path('bookmark/<int:pk>/article/', views.bookmark_article, name='bookmark_article'),
    path('comments/<int:pk>/newsletter/', views.comment_newsletter, name='comment_newsletter'),
    path('like/<int:pk>/newsletter/', views.like_newsletter, name='like_newsletter'),
    path('dislike/<int:pk>/newsletter/', views.dislike_newsletter, name='dislike_newsletter'),
    path('bookmark/<int:pk>/newsletter/', views.bookmark_newsletter, name='bookmark_newsletter'),
]
