from django.template import Library

register = Library()

@register.filter
def sity_count(post, sity):
    count = post.get_sity_count(sity)
    return count


@register.filter
def c_sity_count(community, sity):
    count = community.get_sity_count(sity)
    return count

@register.filter
def u_sity_count(user, sity):
    count = user.get_sity_count(sity)
    return count
