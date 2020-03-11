from django import template
from django.http import HttpResponse
register=template.Library()


@register.filter
def item_view_plus(user_id, item_id):
    from common.utils import item_views_plus

    item_views_plus(user_id, item_id)
    return HttpResponse('Программа сработала!')
