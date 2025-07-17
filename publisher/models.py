from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=255)
    editors = models.ManyToManyField(CustomUser, 
                                     limit_choices_to={'role': 'editor'},
                                     related_name='editor_pub')
    journalist = models.ManyToManyField(CustomUser,
                                        limit_choices_to={'role': 'journalist'},
                                        related_name='journalist_pub')
    
    def __str__(self):
        return f"Name:{self.name}"