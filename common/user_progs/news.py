from django.db.models import Q
from notify.models import Notify


def get_timeline_posts(user_id):
    """ лента записей, которые публикуются друзьями, источниками подписки, сообществами пользователя """
    select_related = ('creator', 'community')
    query = Q(creator_id=user_id)| \
            Q(creator_id__in=self.get_user_notify_ids())| \
            Q(community_id__in=self.get_community_notify_ids())
    query.add(Q(user_set__isnull=True, object_set__isnull=True, status="R"), Q.AND)
    return Notify.objects.filter(query)
