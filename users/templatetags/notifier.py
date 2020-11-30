from django import template
register=template.Library()


@register.filter
def community_notify_count(community, user_id):
    return community.count_community_unread_notify(user_id)
