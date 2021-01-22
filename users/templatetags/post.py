from django import template
register=template.Library()


@register.filter
def get_user_attach(post, request_user):
    return post.get_u_attach(request_user)

@register.filter
def get_community_attach(post, request_user):
    return post.get_c_attach(request_user)
