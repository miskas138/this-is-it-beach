from django import template

register = template.Library()

from django.contrib.auth.models import Group

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()
