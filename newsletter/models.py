from django.db import models
from accounts.models import CustomUser
# from article.models import Publisher


# Create your models here.
class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    publisher = models.ManyToManyField(CustomUser, 
                                       limit_choices_to={'role': 'publisher'}, 
                                       related_name='newsletters_pub')
    journalist = models.ForeignKey(CustomUser,
                                   on_delete=models.CASCADE, 
                                   limit_choices_to={'role': 'journalist'}, 
                                   related_name='newsletters_jour')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"title:{self.title}, publisher:{self.publisher.name}"
    
    class Meta:
        permissions = (
            ('newsletter_create', 'Can create newsletter'),
            ('newsletter_list', 'Can view newsletters'),
            ('newsletter_update', 'Can update newsletter'),
            ('newsletter_delete', 'Can delete newsletter'),
        )