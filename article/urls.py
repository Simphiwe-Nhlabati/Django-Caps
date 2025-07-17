from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/articles', views.Article_View_API, basename='article_api')
router.register(r'api/articles/detail', views.Article_Detail_API, basename='article_detail_api')
# router.register(r'articles/create', views.Article_Generate, basename='article_create')
# router.register(r'articles/(?P<pk>\d+)/update', views.Article_Update, basename='article_update')
# router.register(r'articles/(?P<pk>\d+)/delete', views.Article_Delete, basename='article_delete')

urlpatterns = [
    path('apl/', include(router.urls)),
    path('api/articles/', views.Article_View_API.as_view({'get': 'list'}), name='article_list_api'),
    path('api/articles/detail/', views.Article_Detail_API.as_view({'get': 'list'}), name='article_detail_api'),
    path('articles/', views.Article_View.as_view(), name='article_list'),
    path('articles/<int:pk>/detail/', views.Article_Detail.as_view(), name='article_detail'),
    path('articles/create/', views.Article_Generate.as_view(), name='article_create'),
    path('articles/<int:pk>/update/', views.Article_Update.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', views.Article_Delete.as_view(), name='article_delete'),
]