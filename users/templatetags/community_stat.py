from django import template
register=template.Library()


@register.filter
def count_views_user(community, user_id):
    count = community.count_user_visits(user_id)
    return count
