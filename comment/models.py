from django.db import models
from django.conf import settings
from article.models import Article
from newsletter.models import Newsletter


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article', 'newsletter')


class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article', 'newsletter')


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'article', 'newsletter')