from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from article.models import Article
from newsletter.models import Newsletter
from django.contrib import messages


# Create your views here.
def verify_editor(account):
    return account.position == 'editor' or account.groups.filter(name='Editor').exists()


@login_required
def dashboard_editor(request):
    articles = Article.objects.filter(approved=False)
    newsletters = Newsletter.objects.filter(approved=False)
    
    if not verify_editor(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home_view')
    
    return render(request, 'editor/editor_dashboard.html', {'articles': articles,'newsletters': newsletters})


@login_required
def approve_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.approved = True
    article.save()
    messages.success(request, f'Article "{article.title}" has been approved.')
    return redirect('dashboard_editor')


@login_required
def approve_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.approved = True
    newsletter.save()
    messages.success(request, f'Newsletter "{newsletter.title}" has been approved.')
    return redirect('dashboard_editor')