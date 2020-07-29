from django import template
register=template.Library()


@register.filter
def is_you_block(request_user, user_id):
    if request_user.is_blocked_with_user_with_id(user_id=user_id):
        return True
    else:
        return False
