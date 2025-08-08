from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings


# Create your models here.
class CustomUser(AbstractUser):
    
    USER_CHOICES = (
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    )
    
    position = models.CharField(
        max_length=20,
        choices=USER_CHOICES
    )
    
    # editor_publishers = models.ManyToManyField('self', symmetrical=False, related_name='editors', limit_choices_to={'position': 'publisher'})
    # journalist_publishers = models.ManyToManyField('self', symmetrical=False, related_name='journalists', limit_choices_to={'position': 'publisher'})
    
    subscriptions_publishers = models.ManyToManyField('CustomUser',
                                                      related_name='subscribers_publishers', 
                                                      blank=True)
    
    subscriptions_journalists = models.ManyToManyField('CustomUser', 
                                                       related_name='subscribers_journalists', 
                                                       blank=True, 
                                                       limit_choices_to={'position': 'journalist'})
    
    newsletter_independently = models.ManyToManyField('article.Article', 
                                                      blank=True, 
                                                      related_name='journalist_newsletters')
    
    article_independently = models.ManyToManyField('newsletter.Newsletter', 
                                                   blank=True, 
                                                   related_name='journalist_articles')
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
    )
    
    def position_assign(self):
        if self.position == 'reader':
            self.article_independently = None
            self.newsletter_independently = None
            
        elif self.position == 'journalist':
            self.subscriptions_publishers = None
            self.subscriptions_journalists = None
    
    def __str__(self):
        return f"name:{self.first_name} last name:{self.last_name} username:({self.username})"
   
 
class ResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
   
    def __str__(self):
        return f"user:{self.user} token:{self.token} "