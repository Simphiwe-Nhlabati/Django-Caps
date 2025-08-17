from django.shortcuts import get_object_or_404, redirect
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Newsletter
from .forms import NewsletterForm
from reader.models import Subscriptions
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from article.views import journalist_pem, editor_pem
from notification.models import Notification
from comment.forms import CommentForm
from comment.models import Comment, Bookmark


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
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(newsletter=self.get_object())
        context['likes'] = self.get_object().likes.count()
        context['dislikes'] = self.get_object().dislikes.count()
        context['bookmarked'] = Bookmark.objects.filter(newsletter=self.get_object(), user=self.request.user).exists()
        context['liked'] = self.get_object().likes.filter(pk=self.request.user.pk).exists()
        context['disliked'] = self.get_object().dislikes.filter(pk=self.request.user.pk).exists()

        # Support inline comment editing without JavaScript via ?edit_comment=<id>
        edit_comment_id = self.request.GET.get('edit_comment')
        if edit_comment_id:
            try:
                edit_comment = Comment.objects.get(pk=edit_comment_id, newsletter=self.get_object())
                if edit_comment.user_id == self.request.user.id:
                    context['edit_comment_id'] = edit_comment.pk
                    context['edit_comment_form'] = CommentForm(instance=edit_comment)
            except Comment.DoesNotExist:
                pass

        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # article = self.get_object()
            comment.newsletter = self.get_object()
            comment.user = request.user
            comment.save()
            Notification.objects.create(
                recipient=comment.newsletter.journalist,
                sender=request.user,
                newsletter=comment.newsletter,
                notification_type='comment',
                message=f'{request.user.username} commented on your newsletter: {comment.newsletter.title}'
            )
            messages.success(request, "Comment added successfully.")
            return redirect('newsletter_detail', pk=self.get_object().pk)
        return self.get(request, *args, **kwargs)
    
    
def post(self, request, *args, **kwargs):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.newsletter = self.get_object()
        comment.user = request.user
        comment.save()
        Notification.objects.create(
            recipient=comment.newsletter.journalist,
            sender=request.user,
            newsletter=comment.newsletter,
            notification_type='comment',
            message=f'{request.user.username} commented on your newsletter: {comment.newsletter.title}'
        )
        return redirect('newsletter_detail', pk=self.get_object().pk)
    return self.get(request, *args, **kwargs)

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
    success_url = reverse_lazy('home_view')
    permission_required = 'newsletter.newsletter_create'
    
    def has_permission(self):
        return super().has_permission() and journalist_pem(self.request.user)

    def get_success_url(self):
        return reverse('journalist_dashboard')

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
        if not super().has_permission():
            return False
        newsletter = self.get_object()
        if editor_pem(user):
            return True
        if journalist_pem(user):
            return newsletter.journalist == user
        return False

    def form_valid(self, form):
        messages.success(self.request, "Newsletter updated successfully.")
        return super().form_valid(form)


class Newsletter_Delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Newsletter
    template_name = 'newsletter/newsletter_confirm_delete.html'
    context_object_name = 'newsletter'
    success_url = reverse_lazy('home_view')
    permission_required = 'newsletter.newsletter_delete'

    def has_permission(self):
        user = self.request.user
        if not super().has_permission():
            return False
        newsletter = self.get_object()
        if editor_pem(user):
            return True
        if journalist_pem(user):
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