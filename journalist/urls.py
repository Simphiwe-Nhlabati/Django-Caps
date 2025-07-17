from django.urls import path
from . import views

urlpatterns = [
    path('journalist_dashboard/', views.journalist_dashboard, name='journalist_dashboard'),
]