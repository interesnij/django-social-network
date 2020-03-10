from django import template
from django.http import HttpResponse
register=template.Library()


@register.filter
def item_view_plus(item_id, user_id):
    view = user.item_views_plus(item_id, user_id)
    return HttpResponse('Программа сработала!')
