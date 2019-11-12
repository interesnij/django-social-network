from main.models import Item
from django.http import HttpResponse


def fixed(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_fixed=True
    item.save()
    return HttpResponse("!")


def unfixed(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_fixed=False
    item.save()
    return HttpResponse("!")

def item_delete(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_deleted=True
    item.save()
    return HttpResponse("!")
