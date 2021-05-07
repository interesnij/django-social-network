from django import template
register=template.Library()


@register.filter
def it_is_avatar(photo, user):
    return photo.is_avatar(user)
