from django import template
register=template.Library()


@register.filter
def is_track_exists(user, track_id):
    return user.is_track_exists(track_id)

@register.filter
def is_user_list(user, list):
    return user.is_user_temp_list(list)

@register.filter
def is_user_can_add_list(list, user_id):
    return list.is_user_can_add_list(user_id):
@register.filter
def is_community_can_add_list(list, community_id):
    return list.is_community_can_add_list(community_id)


@register.filter
def item_in_list(list, item_id):
    return list.is_item_in_list(item_id)
