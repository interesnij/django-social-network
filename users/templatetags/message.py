from django import template
register=template.Library()


@register.filter
def get_unread_count(chat, user_id):
    return chat.get_unread_count_message(user_id)

@register.filter
def get_preview_message(chat, user_id):
    return chat.get_preview_message(user_id)

@register.filter
def get_chat_header(chat, user_id):
    return chat.get_header_chat(user_id)

@register.filter
def get_user_attach(message, request_user):
    return message.get_u_attach(request_user)

@register.filter
def get_community_attach(message, request_user):
    return message.get_c_attach(request_user)
