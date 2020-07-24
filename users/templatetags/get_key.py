from django import template
register=template.Library()


@register.filter
def is_track_exists(user, track_id):
    if user.is_track_exists(track_id):
        return True
    else:
        return False

@register.filter
def is_user_list(user, list):
    if user.is_user_temp_list(list):
        return True
    else:
        return False
