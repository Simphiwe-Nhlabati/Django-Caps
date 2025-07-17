from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Newsletter
from .forms import NewsletterForm
from reader.models import Subscriptions
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from article.views import journalist_pem, editor_pem
# from accounts.permissions import JournalistPem, EditorPem


# Create your views here.
class Newsletter_View(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = 'newsletter/newsletter_list.html'
    context_object_name = 'newsletters'
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Newsletter.objects.all()
    
    
class Newsletter_Detail(LoginRequiredMixin, DetailView):
    model = Newsletter
    template_name = 'newsletter/newsletter_detail.html'
    context_object_name = 'newsletter'
    permission_classes = [IsAuthenticated]
    
    def get_object(self, queryset=None):
        return get_object_or_404(Newsletter, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        subscriptions = Subscriptions.objects.filter(user=self.request.user).first()
        subscribed_journalists = subscriptions.journalist.all() if subscriptions else []

        context['subscribed_journalists'] = subscribed_journalists
        return context
    

class Newsletter_View_API(viewsets.ModelViewSet):
    model = Newsletter
    template_name = 'newsletter/newsletter_list.html'
    context_object_name = 'newsletters'
    permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     return Newsletter.objects.all()
    

class Newsletter_Detail_API(viewsets.ModelViewSet):
    model = Newsletter
    template_name = 'newsletter/newsletter_detail.html'
    context_object_name = 'newsletter'
    permission_classes = [IsAuthenticated]
    
    
class Newsletter_Generate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_form.html'
    context_object_name = 'newsletters'
    success_url = reverse_lazy('newsletter_list')
    permission_required = 'newsletter.newsletter_create'

    def form_valid(self, form):
        form.instance.journalist = self.request.user
        messages.success(self.request, "Newsletter created successfully.")
        return super().form_valid(form)


class Newsletter_Update(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_form.html'
    context_object_name = 'newsletters'
    success_url = reverse_lazy('newsletter_list')
    permission_required = 'newsletter.newsletter_update'

    def has_permission(self):
        user = self.request.user
        newsletter = self.get_object()

        if user.has_perm(self.permission_required):
            return True
        elif user.groups.filter(name='Journalist').exists():
            return newsletter.journalist == user
        return False

    def form_valid(self, form):
        messages.success(self.request, "Newsletter updated successfully.")
        return super().form_valid(form)


class Newsletter_Delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Newsletter
    template_name = 'newsletter/newsletter_confirm_delete.html'
    context_object_name = 'newsletter'
    success_url = reverse_lazy('newsletter_list')
    permission_required = 'newsletter.newsletter_delete'

    def has_permission(self):
        user = self.request.user
        newsletter = self.get_object()

        if user.has_perm(self.permission_required):
            return True
        elif user.groups.filter(name='Journalist').exists():
            return newsletter.journalist == user
        return False

    def form_valid(self, form):
        messages.success(self.request, f"Newsletter '{self.object.title}' has been deleted successfully.")
        return super().form_valid(form)
    
    
class Newsletter_Generate_API(CreateAPIView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_form.html'
    success_url = '/newsletters/'
    permission_classes = [IsAuthenticated]
    
    
class Newsletter_Update_API(RetrieveUpdateAPIView):
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_form.html'
    success_url = '/newsletters/'
    permission_classes = [IsAuthenticated]
    

class Newsletter_Delete_API(DestroyAPIView):
    model = Newsletter
    template_name = 'newsletter/newsletter_delete.html'
    success_url = '/newsletters/'
    permission_classes = [IsAuthenticated]