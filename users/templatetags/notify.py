from django import template
register=template.Library()

@register.filter
def get_notify(notify, user):
    return notify.get_notify(user)
