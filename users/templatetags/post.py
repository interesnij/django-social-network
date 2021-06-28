from django import template
register=template.Library()


@register.filter
def get_attach(post, request_user):
    return post.get_attach(request_user)

@register.filter
def get_edit_attach(post, request_user):
    return post.get_edit_attach(request_user)

@register.filter
def u_new_parent(post, request_user):
    return post.get_u_new_parent(request_user)

@register.filter
def c_new_parent(post, request_user):
    return post.get_c_new_parent(request_user)

@register.filter
def u_post_parent(post, request_user):
    return post.get_u_post_parent(request_user)

@register.filter
def c_post_parent(post, request_user):
    return post.get_c_post_parent(request_user)
