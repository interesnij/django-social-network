from django import template
register=template.Library()


@register.filter
def is_you_block(request_user, user_id):
    return request_user.is_blocked_with_user_with_id(user_id=user_id)

@register.filter
def is_can_work_list(request_user, list):
    return request_user.is_can_work_list(list)

@register.filter
def is_user_can_edit_delete(obj, request_user):
    return obj.is_user_can_edit_delete_item(request_user)

@register.filter
def is_user_voted(survey, request_user_id):
    return survey.is_user_voted(request_user_id)

@register.filter
def get_bad_item(item, request_user):
    from common.utils import get_bad_item
    return get_bad_item(item, request_user_id)
