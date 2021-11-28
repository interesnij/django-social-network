from django import template
register=template.Library()


@register.filter
def get_attach(comment, request_user):
    return comment.get_attach(request_user)

@register.filter
def is_admin(request_user, chat_pk):
    return request_user.is_administrator_of_chat(chat_pk)
