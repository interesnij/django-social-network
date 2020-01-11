from django import template
register=template.Library()


@register.filter
def is_track_exists(track_id):
    if request.user.is_track_exists(track_id):
        return True
    else:
        return False
