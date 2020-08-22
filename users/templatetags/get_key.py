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


@register.filter
def track_in_list(list, track_id):
    if list.is_track_in_list(track_id):
        return True
    else:
        return False

@register.filter
def playlist_repost(post):
    return post.parent.post_soundlist.all()[0]

@register.filter
def playlist_repost_creator_pk(post):
    return post.parent.post_soundlist.all()[0].creator.pk

@register.filter
def playlist_repost_creator_name(post):
    return post.playlist_repost().creator.get_full_name()

@register.filter
def playlist_repost_name(post):
    return post.playlist_repost().name

@register.filter
def playlist_repost_pk(post):
    return post.playlist_repost().pk

@register.filter
def playlist_repost_pk(post):
    return post.playlist_repost().pk

@register.filter
def playlist_repost_uuid(post):
    return post.playlist_repost().uuid

@register.filter
def playlist_repost_community(post):
    return post.playlist_repost().community
