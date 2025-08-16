from django.db import models
from django.conf import settings
from article.models import Article
from newsletter.models import Newsletter


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, blank=True, null=True)
    notification_type = models.CharField(max_length=20)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.notification_type} from {self.sender.username} to {self.recipient.username}'