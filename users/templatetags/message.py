from django import template
register=template.Library()


@register.filter
def get_unread_count(chat, user_id):
    return chat.get_unread_count_message(user_id)

@register.filter
def get_preview_message(chat, user_id):
    return chat.get_preview_message(user_id)

@register.filter
def get_header_private_chat(chat, user_id):
    return chat.get_header_private_chat(user_id)
@register.filter
def get_header_group_chat(chat, user_id):
    return chat.get_header_group_chat(user_id)

@register.filter
def get_attach(message, request_user):
    return message.get_attach(request_user)

@register.filter
def is_favourite(message, user_id):
    return message.is_message_in_favourite(user_id)
