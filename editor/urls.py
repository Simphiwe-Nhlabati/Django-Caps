from django.urls import path
from . import views

urlpatterns = [
    path('verify_if_editor/', views.verify_editor, name='verify_editor'),
    path('editor/', views.dashboard_editor, name='dashboard_editor'),
    path('approve/<int:pk>/', views.approve_article, name='approve_article'),
    path('approve_newsletter/<int:pk>/', views.approve_newsletter, name='approve_newsletter'),
]