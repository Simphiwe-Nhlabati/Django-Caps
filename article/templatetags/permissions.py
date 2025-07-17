from django import template

register = template.Library()


@register.filter(name='journalist_pem')
def journalist_pem(user):
    return user.groups.filter(name='Journalist').exists()


@register.filter(name='editor_pem')
def editor_pem(user):
    return user.groups.filter(name='Editor').exists()


@register.filter(name='reader_pem')
def reader_pem(user):
    return user.groups.filter(name='Reader').exists()