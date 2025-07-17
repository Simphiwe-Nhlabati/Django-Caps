from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path("register/", views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('reset_password/', views.reset_password, name='reset_password'),
]