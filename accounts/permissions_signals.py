from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.apps import apps
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    if not created:
        return

    position = instance.position.lower().capitalize()  
    group, _ = Group.objects.get_or_create(name=position)
    instance.groups.add(group)

    if position == 'Reader':
        
        assign_permissions_to_group(group, ['article_list', 'newsletter_list'])

    elif position == 'Editor':
        
        assign_permissions_to_group(group, [
            'article_list', 'article_update', 'article_delete',
            'newsletter_list', 'newsletter_update', 'newsletter_delete'
        ])

    elif position == 'Journalist':
        assign_permissions_to_group(group, [
            'article_create', 'article_list', 'article_update', 'article_delete',
            'newsletter_create', 'newsletter_list', 'newsletter_update', 'newsletter_delete'
        ])


def assign_permissions_to_group(group, codename_list):
    """Assign a list of permission codenames to a group."""
    models = {
        'article': apps.get_model('articles', 'Article'),
        'newsletter': apps.get_model('articles', 'Newsletter'),
    }

    for codename in codename_list:
        
        model_key = codename.split('_')[-1]  
        if model_key not in models:
            continue  

        try:
            permission = Permission.objects.get(
                codename=codename,
                content_type__app_label='articles',
                content_type__model=model_key
            )
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            pass 