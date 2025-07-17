# from django.contrib.auth.models import Permission

# Permission.objects.filter(codename='article_create')

# from django.contrib.auth.models import Group, Permission
# group = Group.objects.get(name='Reader')
# permission = Permission.objects.get(codename='article_list')
# group.permissions.add(permission)


# from django.contrib.auth.models import Group
# from accounts.models import CustomUser
# user = CustomUser.objects.get(username='Simreads650')
# group = Group.objects.get(name='Reader')
# user.groups.all()
# user.get_group_permissions()
# user.get_all_permissions()

# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from article.models import Article

# content_type = ContentType.objects.get_for_model(Article)

# perm = Permission.objects.get(codename='add_article', content_type=content_type)
# group = Group.objects.get(name='Reader')  
# group.permissions.remove(perm)

# from django.contrib.auth.models import Group, Permission

# group = Group.objects.get(name='Reader')
# permissions = Permission.objects.filter(
#     codename__in=[
#         'article_list', 'newsletter_list'
#     ]
# )
# group.permissions.add(*permissions)


# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group, Permission
# reader_group, created = Group.objects.get_or_create(name='Reader')
# User = get_user_model()
# user = User.objects.get(username='Simreads650')  
# reader_group.user_set.add(user)

# from django.contrib.auth import get_user_model
# User = get_user_model()

# user = User.objects.get(username='Simreads650')  
# print(user)

# from django.contrib.auth.models import Group

# reader_group, created = Group.objects.get_or_create(name='Reader')
# reader_group.user_set.add(user)
# reader_group.save()


# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group

# User = get_user_model()


# user = User.objects.get(username='Simreads650')
# group, created = Group.objects.get_or_create(name='Reader')


# user.groups.add(group)

# user.save()
# user.refresh_from_db()

# print(user.groups.all()) 

