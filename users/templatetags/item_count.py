from django.template import Library
from users.model.profile import OneUserLocation

register = Library()

@register.filter
def sity_count(item, sity):
    count = item.get_sity_count(sity)
    return count
