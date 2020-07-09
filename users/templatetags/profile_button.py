from django import template
register=template.Library()


@register.filter
def is_blocked_user(request_user, user_id):
    if request_user.is_authenticated and request_user.has_blocked_user_with_id(user_id):
        return True
    else:
        return False

@register.filter
def is_frend_user(request_user, user_id):
    if request_user.is_authenticated and request_user.is_connected_with_user_with_id(user_id):
        return True
    else:
        return False

@register.filter
def is_request_follow(request_user, user_id):
    if request_user.is_authenticated and request_user.is_following_user_with_id(user_id):
        return True
    else:
        return False

@register.filter
def is_user_follow(request_user, user_id):
    if request_user.is_authenticated and request_user.is_followers_user_with_id(user_id):
        return True
    else:
        return False

@register.filter
def is_following_user(request_user, user_id):
    if request_user.is_authenticated and request_user.is_following_user_with_id(user_id):
        return True
    else:
        return False
