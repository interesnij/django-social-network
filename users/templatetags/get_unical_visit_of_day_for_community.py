from django import template
register=template.Library()
from stst.models import CommunityNumbers


@register.filter
def get_views(day, community_id):
    views = CommunityNumbers.objects.filter(community=community_id, created__day=day).distinct("user").values('platform')
    return len(views)
