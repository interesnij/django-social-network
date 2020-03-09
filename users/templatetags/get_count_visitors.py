from django import template
register=template.Library()


@register.filter
def count_visitor_for_user(user, target):
    return user.get_count_visitor_for_user(target)
