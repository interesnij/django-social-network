from django.template import Library

register = Library()

@register.filter
def sity_count(post, sity):
    return post.get_sity_count(sity)

@register.filter
def c_sity_count(community, sity):
    return community.get_sity_count(sity)

@register.filter
def u_sity_count(user, sity):
    return user.get_sity_count(sity)
