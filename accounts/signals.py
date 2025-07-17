from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from article.models import Article


@receiver(post_save, sender=CustomUser)
def notify_subscriber_email(sender, instance, created, **kwargs):
    
    if not created and instance.approved:
        author = instance.subscriptions_journalists.all()
        publisher = instance.subscriptions_publishers.all()
        
        
        subscriber = set()
        
        if publisher:
            subscriber.update(publisher.publisher_subscribers.all())

            subscriber.update(author.journalist_subscribers.all())

            recipient_emails = [user.email for user in subscriber if user.email]
            if recipient_emails:
                send_mail(
                    subject='New Article Published',
                    message=f'New article "{instance.title}" has been published.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipient_emails,
                    fail_silently=True,
                )
                


