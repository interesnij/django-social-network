from django import template
register=template.Library()


@register.filter
def get_user_attach(comment, request_user):
    return comment.get_u_attach(request_user)

@register.filter
def get_community_attach(comment, request_user):
    return comment.get_c_attach(request_user)
