from django import template
register=template.Library()
from stst.models import CommunityNumbers


@register.filter
def is_track_exists(month):
    views = CommunityNumbers.objects.filter(community=self.community.pk, created__month=month).distinct().values('platform')
    return views
