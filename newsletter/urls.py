from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'newsletters', views.Newsletter_View_API, basename='newsletter_api')
router.register(r'newsletters/detail', views.Newsletter_Detail_API, basename='newsletter_detail')

urlpatterns = [
    path('apl/', include(router.urls)),
    path('api/newsletter/', views.Newsletter_View_API.as_view({'get': 'list'}), name='newsletter_list_api'),
    path('api/newsletter/detail/', views.Newsletter_Detail_API.as_view({'get': 'list'}), name='newsletter_detail_api'),
    path('newsletter/', views.Newsletter_View.as_view(), name='newsletter_list'),
    path('newsletter/<int:pk>/detail/', views.Newsletter_Detail.as_view(), name='newsletter_detail'),
    path('newsletter/create/', views.Newsletter_Generate.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/update/', views.Newsletter_Update.as_view(), name='newsletter_update'),
    path('newsletter/<int:pk>/delete/', views.Newsletter_Delete.as_view(), name='newsletter_delete'),
]