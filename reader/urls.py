from django.urls import path
from . import views

urlpatterns = [
    path('reader_dashboard/', views.reader_dashboard, name='reader_dashboard'),
    path('subscriptions_journalist/<int:pk>/', views.subscriptions_journalist, name='subscriptions_journalist'),
    path('subscriptions_publisher/<int:pk>/', views.subscriptions_publisher, name='subscriptions_publisher'),
]

