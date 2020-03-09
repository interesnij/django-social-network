from django import template
register=template.Library()


@register.filter
def count_visitor_for_user(user, user_id):
    return user.get_count_visitor_for_user(user_id)
