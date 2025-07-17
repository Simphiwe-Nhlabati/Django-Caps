from . import views
from django.urls import path

urlpatterns = [
    path('publisher_home/', views.publisher_home, name='publisher_home'),
]