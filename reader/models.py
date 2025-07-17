from django.db import models
from accounts.models import CustomUser
from article.models import Publisher


# Create your models here.
class Subscriptions(models.Model):
    user = models.ForeignKey(CustomUser, 
                             on_delete=models.CASCADE,
                             related_name='user_subscriptions')
    
    journalist = models.ManyToManyField(CustomUser, 
                                        limit_choices_to={'role': 'journalist'},
                                        related_name='journalist_subscriptions',
                                        blank=True, 
                                        )
    
    publisher = models.ForeignKey(Publisher, 
                                  null=True, 
                                  blank=True, 
                                  on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} has subscribed to {self.journalist}"