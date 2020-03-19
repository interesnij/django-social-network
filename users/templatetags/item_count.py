from django.template import Library

register = Library()

@register.filter
def sity_count(item, sity):
    count = item.get_sity_count(sity)
    return count


@register.filter
def c_sity_count(community, sity):
    count = community.get_sity_count(sity)
    return count
