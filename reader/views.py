from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from accounts.models import CustomUser
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
# from accounts.permissions import ReaderPem
from rest_framework.response import Response
from article.models import Article
from newsletter.models import Newsletter
from article.serializers import ArticleSerializer
from .models import Subscriptions


# Create your views here.
class SubscriptionView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
    
        if user.position == 'reader':
            publisher = user.subscriptions_publisher.value_list('id', flat=True)
            journalist = user.subscriptions_journalist.value_list('id', flat=True)
            
            articles = Article.objects.filter(
                is_approved=True
            ).filter(
                publisher__id__in=publisher
            ) | Article.objects.filter(
                is_approved=True,
                author__id__in=journalist)
            
            serializer_class = ArticleSerializer(Article, many=True)
            articles = articles.distinct('-created_at')
            return Response(serializer_class.data)
        
        return Response('Readers only')
            

def reader_dashboard(request):
    articles = Article.objects.all()
    newsletters = Newsletter.objects.all()
    subscriptions = Subscriptions.objects.filter(user=request.user).first()
    # subs_journalist = Subscriptions.objects.filter(user=request.user, journalist__isnull=False)
    subs_journalist = subscriptions.journalist.all() if subscriptions else []
    subs_publisher = Subscriptions.objects.filter(user=request.user, publisher__isnull=False)
    context = {
        'articles': articles,
        'newsletters': newsletters,
        'subs_journalist': subs_journalist,
        'subs_publisher': subs_publisher
    }
    return render(request, 'reader/reader_dashboard.html', {'context': context})


@login_required
def subscriptions_journalist(request, pk):
    # journalist = get_object_or_404(CustomUser, pk=pk, position='journalist')
    journalist = get_object_or_404(CustomUser, pk=pk)
    subscriptions, created = Subscriptions.objects.get_or_create(user=request.user)
    
    
    if request.method == 'POST':
        if journalist in subscriptions.journalist.all():
            subscriptions.journalist.remove(journalist)
            messages.success(request, f'Unsubscribed from {journalist.username}')
        else:
            subscriptions.journalist.add(journalist)
            messages.success(request, f'Subscribed to {journalist.username}')
        return redirect('reader_dashboard')
    
    return render(request, 'subscriptions_journalist.html', {'journalist': journalist})

    # journalist = get_object_or_404(User, pk=pk, role='journalist')
    # request.user.subscribed_journalists.add(journalist)
    # messages.success(request, f'Subscribed to journalist: {journalist.username}')
    # return redirect('subscription-dashboard')
    

@login_required
def unsubscriptions_journalist(request, pk):
    journalist = get_object_or_404(CustomUser, pk=pk, position='journalist')
    request.user.subscribed_journalists.remove(journalist)
    messages.success(request, f'Unsubscribed from journalist: {journalist.username}')
    return redirect('subscription-dashboard')


@login_required
def subscriptions_publisher(request, pk):
    publisher = get_object_or_404(CustomUser, pk=pk, position='publisher')
    if request.method == 'POST':
        if request.user in publisher.subscribers.all():
            publisher.subscribers.remove(request.user)
            messages.success(request, f'You have unsubscribed from {publisher.username}.')
        else:
            publisher.subscribers.add(request.user)
            messages.success(request, f'You have subscribed to {publisher.username}.')
        return redirect('subscriptions_publisher', pk=pk)
    
    return render(request, 'subscriptions_publisher.html', {'publisher': publisher})

    # publisher = get_object_or_404(User, pk=pk, role='publisher')
    # request.user.subscribed_publishers.add(publisher)
    # messages.success(request, f'Subscribed to publisher: {publisher.username}')
    # return redirect('subscription-dashboard')
    

@login_required
def unsubscriptions_publisher(request, pk):
    publisher = get_object_or_404(CustomUser, pk=pk, role='publisher')
    request.user.subscribed_publishers.remove(publisher)
    messages.success(request, f'Unsubscribed from publisher: {publisher.username}')
    return redirect('reader_dashboard')