from django import template
register=template.Library()


@register.filter
def is_track_exists(track_id): 
    try:
        true = request.user.is_track_exists(track_id)
        return True
    except:
        return False
    return dictionary.get(key)
