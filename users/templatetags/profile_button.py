from django import template
register=template.Library()


@register.filter
def is_blocked_user(user, request_user):
    try:
        user.is_authenticated and request_user.has_blocked_user_with_id(request_user)
        return True
    except:
        return False

@register.filter
def is_request_follow(user, request_user):
    try:
        Follow.objects.get(followed_user=user,user=request_user)
        return True
    except:
        return False

@register.filter
def is_user_follow(user, request_user):
    try:
        Follow.objects.get(followed_user=request_user,user=user)
        return True
    except:
        return False
