from django.template import Library
from users.model.profile import OneUserLocation

register = Library()

@register.filter
def sity_count(model):
    try:
        link = OneUserLocation.objects.get(user__pk=user_id, city_ru=sity)
        return link.count
    except:
        pass
