from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
# from django.urls import reverse_lazy
from .models import Article
from .forms import ArticleForm
from reader.models import Subscriptions
# from accounts.permissions import JournalistPem, EditorPem
from .serializers import ArticleSerializer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from accounts.models import CustomUser
from django.contrib import messages
# from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
# from django import template


# register = template.Library()


# Create your views here.
# @register.filter(name='journalist_pem')
def journalist_pem(user):
    return user.groups.filter(name='Journalist').exists()


# @register.filter(name='editor_pem')
def editor_pem(user):
    return user.groups.filter(name='Editor').exists()


# @register.filter(name='reader_pem')
def reader_pem(user):
    return user.groups.filter(name='Reader').exists()


class Article_View(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'articles'
    serializer_class = ArticleSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Article.objects.all()
    

class Article_Detail(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article/article_detail.html'
    context_object_name = 'article'
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self, queryset=None):
        return get_object_or_404(Article, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        subscriptions = Subscriptions.objects.filter(user=self.request.user).first()
        subscribed_journalists = subscriptions.journalist.all() if subscriptions else []

        context['subscribed_journalists'] = subscribed_journalists
        return context


class Article_View_API(viewsets.ModelViewSet):
    # model = Publisher
    template_name = 'article/article_list.html'
    context_object_name = 'articles'
    serializer_class = ArticleSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Article.objects.all()
    
    def get_journalist(self, obj):
        return obj.journalist.username if obj.journalist else None
    
    
class Article_Detail_API(viewsets.ModelViewSet):
    # model = Publisher
    template_name = 'article/article_detail.html'
    context_object_name = 'articles'
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self, queryset=None):
        return get_object_or_404(Article)
    
    
class Article_Generate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/article_form.html'
    context_object_name = 'articles'
    success_url = reverse_lazy('article_list')
    permission_required = 'article.article_create'

    def has_permission(self):
        return super().has_permission() and journalist_pem(self.request.user)

    def get_success_url(self):
        return reverse('journalist_dashboard')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.publisher = self.request.user
        article.journalist = self.request.user
        article.is_approved = False
        article.save()
        messages.success(self.request, "Article created successfully and waiting for editor approval.")
        return redirect(self.get_success_url())


class Article_Update(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/article_form.html'
    context_object_name = 'articles'
    success_url = reverse_lazy('home_view')
    permission_required = 'article.article_update'

    def has_permission(self):
        user = self.request.user
        if not super().has_permission():
            return False
        article = self.get_object()
        if editor_pem(user):
            return True
        if journalist_pem(user):
            return article.journalist == user
        return False

    def form_valid(self, form):
        if journalist_pem(self.request.user) and self.get_object().approved and form.instance.approved:
            form.instance.is_approved = False
        messages.success(self.request, "Article updated successfully.")
        return super().form_valid(form)


class Article_Delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = 'article/article_delete.html'
    context_object_name = 'articles'
    success_url = reverse_lazy('article_list')
    permission_required = 'article.article_delete'

    def has_permission(self):
        user = self.request.user
        if not super().has_permission():
            return False
        article = self.get_object()
        if editor_pem(user):
            return True
        if journalist_pem(user):
            return article.journalist == user
        return False

    def form_valid(self, form):
        messages.success(self.request, f"Article '{self.object.title}' deleted successfully.")
        return super().form_valid(form)


# @api_view(['POST'])   
class Article_Generate_API(CreateAPIView):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    # success_url = reverse_lazy('article_list')
    
    def perform_create(self, serializer):
        serializer.save(journalist=self.request.user.customuser)
        
    
# @api_view(['GET', 'PUT'])   
class Article_Update_API(RetrieveUpdateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    

# @api_view(['GET', 'DELETE'])
class Article_Delete_API(DestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    


    
    
    

    
    

    

    