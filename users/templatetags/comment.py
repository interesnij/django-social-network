from django import template
register=template.Library()


@register.filter
def get_attach(comment, request_user):
    return comment.get_attach(request_user)
