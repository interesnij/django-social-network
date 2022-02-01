from django import template
register=template.Library()


@register.filter
def is_user_list(list, user):
    return list.is_user_list(user)

@register.filter
def is_user_collection_list(list, user_id):
    return list.is_user_collection_list(user_id)

@register.filter
def is_community_list(list, user):
    return list.is_community_list(user)

@register.filter
def is_community_collection_list(list, community_id):
    return list.is_community_collection_list(community_id)
