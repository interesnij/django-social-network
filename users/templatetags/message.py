from django import template
register=template.Library()


@register.filter
def get_unread_count(chat, user_id):
    return chat.get_unread_count_message(user_id)

@register.filter
def get_name(chat, user_id):
    return chat.get_name(user_id)


@register.filter
def is_can_send_message(user, request_user_id):
    return user.is_user_can_send_message(request_user_id)

@register.filter
def is_read(message, user_id):
    return message.is_copy_reed(user_id)

@register.filter
def get_preview_text(message, user_id):
    return message.get_preview_text(user_id)

@register.filter
def get_preview_message(chat, user_id):
    return chat.get_preview_message(user_id)

@register.filter
def get_attach(message, request_user):
    return message.get_attach(request_user)

@register.filter
def is_favourite(message, user_id):
    return message.is_favourite(user_id)

@register.filter
def get_edit_attach(message, request_user):
    return message.get_edit_attach(request_user)


@register.filter
def is_admin(user, chat_pk):
    return user.is_administrator_of_chat(chat_pk)

@register.filter
def liked_manager(user, chat):
    from common.model.votes import SupportUserVotes
    return SupportUserVotes.objects.filter(user=user, manager=chat.get_chat_member(user.id), vote=SupportUserVotes.LIKE)

@register.filter
def disliked_manager(user, chat):
    from common.model.votes import SupportUserVotes
    return SupportUserVotes.objects.filter(user=user, manager=chat.get_chat_member(user.id), vote=SupportUserVotes.DISLIKE)
