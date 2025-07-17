from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


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
    

# @receiver(post_save, sender=CustomUser)        
# def assign_user_to_group(sender, instance, created, **kwargs):
#     if created:
#         group_name = instance.position.capitalize()
#         group, created = Group.objects.get_or_create(name=group_name)
#         instance.groups.add(group)

#         if group_name == 'Reader':
#             # Can only view articles and newsletters.
#             article_model = apps.get_model('article', 'Article')
#             newsletter_model = apps.get_model('article', 'Newsletter')

#             view_article_permission = Permission.objects.get(codename='article_list', content_type__app_label='articles', content_type__model='article')
#             view_newsletter_permission = Permission.objects.get(codename='newsletter_list', content_type__app_label='articles', content_type__model='newsletter')

#             group.permissions.add(view_article_permission, view_newsletter_permission)

#         elif group_name == 'Editor':
#             # Can view, update, and delete articles and newsletters.
#             article_model = apps.get_model('articles', 'Article')
#             newsletter_model = apps.get_model('articles', 'Newsletter')

#             view_article_permission = Permission.objects.get(codename='article_list', content_type__app_label='articles', content_type__model='article')
#             change_article_permission = Permission.objects.get(codename='article_update', content_type__app_label='articles', content_type__model='article')
#             delete_article_permission = Permission.objects.get(codename='article_delete', content_type__app_label='articles', content_type__model='article')

#             view_newsletter_permission = Permission.objects.get(codename='newsletter_list', content_type__app_label='articles', content_type__model='newsletter')
#             change_newsletter_permission = Permission.objects.get(codename='newsletter_update', content_type__app_label='articles', content_type__model='newsletter')
#             delete_newsletter_permission = Permission.objects.get(codename='newsletter_delete', content_type__app_label='articles', content_type__model='newsletter')

#             group.permissions.add(
#                 view_article_permission, change_article_permission, delete_article_permission,
#                 view_newsletter_permission, change_newsletter_permission, delete_newsletter_permission
#             )

#         elif group_name == 'Journalist':
#             # Can create, view, update, and delete articles and newsletters.
#             article_model = apps.get_model('articles', 'Article')
#             newsletter_model = apps.get_model('articles', 'Newsletter')

#             add_article_permission = Permission.objects.get(codename='article_create', content_type__app_label='articles', content_type__model='article')
#             view_article_permission = Permission.objects.get(codename='article_list', content_type__app_label='articles', content_type__model='article')
#             change_article_permission = Permission.objects.get(codename='article_update', content_type__app_label='articles', content_type__model='article')
#             delete_article_permission = Permission.objects.get(codename='article_delete', content_type__app_label='articles', content_type__model='article')

#             add_newsletter_permission = Permission.objects.get(codename='newsletter_create', content_type__app_label='articles', content_type__model='newsletter')
#             view_newsletter_permission = Permission.objects.get(codename='newsletter_list', content_type__app_label='articles', content_type__model='newsletter')
#             change_newsletter_permission = Permission.objects.get(codename='newsletter_update', content_type__app_label='articles', content_type__model='newsletter')
#             delete_newsletter_permission = Permission.objects.get(codename='newsletter_delete', content_type__app_label='articles', content_type__model='newsletter')

#             group.permissions.add(
#                 add_article_permission, view_article_permission, change_article_permission, delete_article_permission,
#                 add_newsletter_permission, view_newsletter_permission, change_newsletter_permission, delete_newsletter_permission
#             )
   
 
class ResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
   
    def __str__(self):
        return f"user:{self.user} token:{self.token} "