from django import template
register=template.Library()


@register.filter
def it_is_avatar(photo, user):
    if photo.is_avatar(user):
        return True
    else:
        return False
