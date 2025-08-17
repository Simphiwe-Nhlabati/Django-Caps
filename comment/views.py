from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from article.models import Article
from newsletter.models import Newsletter
from .models import Bookmark
from notification.models import Notification
from comment.forms import CommentForm
from comment.models import Comment
from django.shortcuts import render
from django.contrib import messages


@login_required
def comment_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            
            # Create the notification
            Notification.objects.create(
                recipient=article.journalist,
                sender=request.user,
                article=article,
                notification_type='comment',
                message=f'{request.user.username} commented on your article: {article.title}'
            )
            
            # Redirect to the article detail page after a successful comment
            return redirect('article_detail', pk=pk)
        
        # If the form is NOT valid, you need to re-render the page with the form errors.
        else:
            # You must get the context data to render the page correctly
            context = {
                'article': article,
                'form': form, # Pass the form with validation errors back to the template
                'comments': Comment.objects.filter(article=article) # and any other context
            }
            return render(request, 'article_detail.html', context)
            
    else:  # This block handles GET requests
        form = CommentForm()
    
    # This section handles the initial GET request
    context = {
        'article': article,
        'form': form,
        'comments': Comment.objects.filter(article=article),
        # Add any other context variables your template needs
    }
    return render(request, 'article_detail.html', context)


@login_required
def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
        if article.dislikes.filter(id=request.user.id).exists():
            article.dislikes.remove(request.user)
        Notification.objects.create(
            recipient=article.journalist,
            sender=request.user,
            article=article,
            notification_type='like',
            message=f'{request.user.username} liked your article: {article.title}'
        )
    return redirect('article_detail', pk=pk)


@login_required
def dislike_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.dislikes.filter(id=request.user.id).exists():
        article.dislikes.remove(request.user)
    else:
        article.dislikes.add(request.user)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
        Notification.objects.create(
            recipient=article.journalist,
            sender=request.user,
            article=article,
            notification_type='dislike',
            message=f'{request.user.username} disliked your article: {article.title}'
        )
    return redirect('article_detail', pk=pk)


@login_required
def bookmark_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if Bookmark.objects.filter(article=article, user=request.user).exists():
        Bookmark.objects.filter(article=article, user=request.user).delete()
    else:
        Bookmark.objects.create(article=article, user=request.user)
    return redirect('article_detail', pk=pk)


@login_required
def comment_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.newsletter = newsletter
            comment.user = request.user
            comment.save()
            Notification.objects.create(
                recipient=newsletter.journalist,
                sender=request.user,
                newsletter=newsletter,
                notification_type='comment',
                message=f'{request.user.username} commented on your newsletter: {newsletter.title}'
            )
            return redirect('newsletter_detail', pk=pk)
    else:
        form = CommentForm()
    return redirect('newsletter_detail', pk=pk)


@login_required
def like_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if newsletter.likes.filter(id=request.user.id).exists():
        newsletter.likes.remove(request.user)
    else:
        newsletter.likes.add(request.user)
        if newsletter.dislikes.filter(id=request.user.id).exists():
            newsletter.dislikes.remove(request.user)
        Notification.objects.create(
            recipient=newsletter.journalist,
            sender=request.user,
            newsletter=newsletter,
            notification_type='like',
            message=f'{request.user.username} liked your newsletter: {newsletter.title}'
        )
    return redirect('newsletter_detail', pk=pk)


@login_required
def dislike_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if newsletter.dislikes.filter(id=request.user.id).exists():
        newsletter.dislikes.remove(request.user)
    else:
        newsletter.dislikes.add(request.user)
        if newsletter.likes.filter(id=request.user.id).exists():
            newsletter.likes.remove(request.user)
        Notification.objects.create(
            recipient=newsletter.journalist,
            sender=request.user,
            newsletter=newsletter,
            notification_type='dislike',
            message=f'{request.user.username} disliked your newsletter: {newsletter.title}'
        )
    return redirect('newsletter_detail', pk=pk)


@login_required
def bookmark_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if Bookmark.objects.filter(newsletter=newsletter, user=request.user).exists():
        Bookmark.objects.filter(newsletter=newsletter, user=request.user).delete()
    else:
        Bookmark.objects.create(newsletter=newsletter, user=request.user)
    return redirect('newsletter_detail', pk=pk)


@login_required
def edit_comment_article(request, pk):
    """Edit an existing comment on an article. Only the comment owner can edit."""
    comment = get_object_or_404(Comment, pk=pk)
    if not comment.article:
        messages.error(request, 'Invalid comment reference.')
        return redirect('home_view')

    if request.user != comment.user:
        messages.error(request, 'You are not allowed to edit this comment.')
        return redirect('article_detail', pk=comment.article.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
        else:
            messages.error(request, 'Please correct the errors in the form.')
        return redirect('article_detail', pk=comment.article.pk)

    # For non-POST requests, redirect back to the article detail
    return redirect('article_detail', pk=comment.article.pk)


@login_required
def delete_comment_article(request, pk):
    """Delete an existing comment on an article. Only the comment owner can delete."""
    comment = get_object_or_404(Comment, pk=pk)
    if not comment.article:
        messages.error(request, 'Invalid comment reference.')
        return redirect('home_view')

    if request.user != comment.user:
        messages.error(request, 'You are not allowed to delete this comment.')
        return redirect('article_detail', pk=comment.article.pk)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    return redirect('article_detail', pk=comment.article.pk)


@login_required
def edit_comment_newsletter(request, pk):
    """Edit an existing comment on a newsletter. Only the comment owner can edit."""
    comment = get_object_or_404(Comment, pk=pk)
    if not comment.newsletter:
        messages.error(request, 'Invalid comment reference.')
        return redirect('home_view')

    if request.user != comment.user:
        messages.error(request, 'You are not allowed to edit this comment.')
        return redirect('newsletter_detail', pk=comment.newsletter.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
        else:
            messages.error(request, 'Please correct the errors in the form.')
        return redirect('newsletter_detail', pk=comment.newsletter.pk)

    return redirect('newsletter_detail', pk=comment.newsletter.pk)


@login_required
def delete_comment_newsletter(request, pk):
    """Delete an existing comment on a newsletter. Only the comment owner can delete."""
    comment = get_object_or_404(Comment, pk=pk)
    if not comment.newsletter:
        messages.error(request, 'Invalid comment reference.')
        return redirect('home_view')

    if request.user != comment.user:
        messages.error(request, 'You are not allowed to delete this comment.')
        return redirect('newsletter_detail', pk=comment.newsletter.pk)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    return redirect('newsletter_detail', pk=comment.newsletter.pk)