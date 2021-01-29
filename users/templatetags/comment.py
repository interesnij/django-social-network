from django import template
register=template.Library()


@register.filter
def get_user_attach(message, request_user):
    return message.get_u_attach(request_user)

@register.filter
def get_community_attach(message, request_user):
    return message.get_c_attach(request_user)
