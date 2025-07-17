from django.db import models
from accounts.models import CustomUser
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


# Create your models here.
class Publisher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='publisher')
    name = models.CharField(max_length=100)
    editors = models.ManyToManyField('accounts.CustomUser', 
                                     limit_choices_to={'position': 'editor'}, 
                                     related_name='editor_publishers')
    journalists = models.ManyToManyField('accounts.CustomUser', 
                                         limit_choices_to={'position': 'journalist'}, 
                                         related_name='journalist_publishers')
    
    def __str__(self):
        return f"name:{self.name}"
    

class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    content = models.TextField()
    publisher = models.ForeignKey(CustomUser, 
                                  on_delete=models.CASCADE, 
                                  related_name='articles_published')
    journalist = models.ForeignKey(CustomUser, 
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   blank=True,
                                   limit_choices_to={'position': 'journalist'},
                                   related_name='articles_journalist')
    editors = models.ManyToManyField(CustomUser, 
                                     limit_choices_to={'position': 'editor'}, 
                                     related_name='article_editors')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"title:{self.title}, journalist:{self.journalist}"
    
    class Meta:
        permissions = (
            ('article_create', 'Can create article'),
            ('article_list', 'Can view articles'),
            ('article_update', 'Can update article'),
            ('article_delete', 'Can delete article'),
        )
    

