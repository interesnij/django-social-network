from django import template
register=template.Library()


@register.filter
def is_you_block(request_user, user_id):
    return request_user.is_blocked_with_user_with_id(user_id=user_id)

@register.filter
def is_can_work_list(request_user, list):
    return request_user.is_can_work_list(list)
