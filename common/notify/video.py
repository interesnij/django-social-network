from datetime import date
today = date.today()
from common.notify.progs import *


def user_video_notify(creator, recipient_id, action_community_id, video_id, comment_id, list_id, socket_name, verb):
    from notify.model.video import VideoNotify

    current_verb = creator.get_verb_gender(verb)
    if action_community_id:
        if VideoNotify.objects.filter(community_id=action_community_id, video_id=video_id, verb=verb).exists():
            pass
        elif VideoNotify.objects.filter(community_id=action_community_id, recipient_id=recipient_id, created__gt=today, verb=verb).exists():
            notify = VideoNotify.objects.get(community_id=action_community_id, recipient_id=recipient_id, created__gt=today, verb=verb)
            VideoNotify.objects.create(creator=creator, community_id=action_community_id, recipient_id=recipient_id, video_id=video_id, verb=verb, user_set=notify)
        elif VideoNotify.objects.filter(recipient_id=recipient_id, community__isnull=False, video_id=video_id, created__gt=today, verb=verb).exists():
            notify = VideoNotify.objects.get(recipient_id=recipient_id, community__isnull=False, video_id=video_id, created__gt=today, verb=verb)
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, community_id=action_community_id, video_id=video_id, verb="G"+verb, object_set=notify)
        else:
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, community_id=action_community_id, video_id=video_id, verb=verb)
        user_send(video_id, recipient_id, action_community_id, socket_name)
    elif comment_id:
        if VideoNotifyVideoNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif VideoNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exists():
            notify = VideoNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, video_id=video_id, verb=current_verb, user_set=notify)
        elif VideoNotify.objects.filter(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb).exists():
            notify = VideoNotify.objects.get(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb)
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, video_id=video_id, comment_id=comment_id, verb="G"+verb, object_set=notify)
        else:
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, video_id=video_id, comment_id=comment_id, verb=current_verb)
        user_send(comment_id, recipient_id, None, socket_name)
    elif list_id:
        if VideoNotify.objects.filter(creator=creator, list_id=list_id, verb=current_verb).exists():
            pass
        elif VideoNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exists():
            notify = VideoNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=current_verb, user_set=notify)
        elif VideoNotify.objects.filter(recipient_id=recipient_id, list_id=list_id, created__gt=today, verb=verb).exists():
            notify = VideoNotify.objects.get(recipient_id=recipient_id, list_id=list_id, created__gt=today, verb=verb)
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb="G"+verb, object_set=notify)
        else:
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=current_verb)
        user_send(list_id, recipient_id, None, socket_name)
    else:
        from django.db.models import Q
        if VideoNotify.objects.filter(creator=creator, video_id=video_id, community__isnull=True, verb=current_verb).exists():
            pass
        elif VideoNotify.objects.filter(creator=creator, recipient_id=recipient_id, community__isnull=True, created__gt=today, verb=current_verb).exists():
            notify = VideoNotify.objects.filter(creator=creator, recipient_id=recipient_id, community__isnull=True, created__gt=today, verb=current_verb).last()
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, video_id=video_id, verb=current_verb, user_set=notify)
        elif VideoNotify.objects.filter(Q(verb=verb)|Q(verb="W"+verb), recipient_id=recipient_id, community__isnull=True, created__gt=today, video_id=video_id).exists():
            notify = VideoNotify.objects.get(Q(verb=verb)|Q(verb="W"+verb), recipient_id=recipient_id, community__isnull=True, video_id=video_id, created__gt=today)
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, video_id=video_id, verb="G"+verb, object_set=notify)
        else:
            VideoNotify.objects.create(creator=creator, recipient_id=recipient_id, video_id=video_id, verb=current_verb)
        user_send(video_id, recipient_id, None, socket_name)

def community_video_notify(creator, community, action_community_id, video_id, comment_id, list_id, socket_name, verb):
    from notify.model.video import VideoCommunityNotify

    current_verb = creator.get_verb_gender(verb)
    if action_community_id:
        if VideoCommunityNotify.objects.filter(community_creator_id=action_community_id, video_id=video_id, verb=verb).exists():
            pass
        elif VideoCommunityNotify.objects.filter(community_id=community.pk, community_creator_id=action_community_id, created__gt=today, verb=verb).exists():
            notify = VideoCommunityNotify.objects.get(community_id=community.pk, community_creator_id=action_community_id, created__gt=today, verb=verb)
            VideoCommunityNotify.objects.create(creator=creator, community_id=community.pk, community_creator_id=action_community_id, video_id=video_id, verb=verb, user_set=notify)
        elif VideoCommunityNotify.objects.filter(community_id=community_id, video_id=video_id, created__gt=today, verb=verb).exists():
            notify = VideoCommunityNotify.objects.get(community_id=community_id, video_id=video_id, created__gt=today, verb=verb)
            VideoCommunityNotify.objects.create(creator=creator, community_creator_id=action_community_id, community_id=community.pk, video_id=video_id, verb="G"+verb, object_set=notify)
        else:
            VideoCommunityNotify.objects.create(creator=creator, community_creator_id=action_community_id, community_id=community.pk, video_id=video_id, verb=verb)
        community_send(video_id, community, action_community_id, socket_name)
    elif comment_id:
        if VideoCommunityNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif VideoCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).exists():
            notify = VideoCommunityNotify.objects.get(creator=creator, community_id=community.id, created__gt=today, verb=current_verb)
            VideoCommunityNotify.objects.create(creator=creator, community_id=community.id, video_id=video_id, verb=current_verb, user_set=notify)
        elif VideoCommunityNotify.objects.filter(community_id=community.id, comment_id=comment_id, created__gt=today, verb=verb).exists():
            notify = VideoCommunityNotify.objects.get(community_id=community.id, comment_id=comment_id, created__gt=today, verb=verb)
            VideoCommunityNotify.objects.create(creator=creator, community_id=community.id, video_id=video_id, comment_id=comment_id, verb="G"+verb, object_set=notify)
        else:
            VideoCommunityNotify.objects.create(creator=creator, community_id=community.id, video_id=video_id, comment_id=comment_id, verb=current_verb)
        community_send(comment_id, community, None, socket_name)
    elif list_id:
        if VideoCommunityNotify.objects.filter(creator=creator, list_id=list_id, verb=current_verb).exists():
            pass
        elif VideoCommunityNotify.objects.filter(creator=creator, community_id=community_id, created__gt=today, verb=current_verb).exists():
            notify = VideoCommunityNotify.objects.get(creator=creator, community_id=community_id, created__gt=today, verb=current_verb)
            VideoCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=current_verb, user_set=notify)
        elif VideoCommunityNotify.objects.filter(community_id=community_id, list_id=list_id, created__gt=today, verb=verb).exists():
            notify = VideoCommunityNotify.objects.get(community_id=community_id, list_id=list_id, created__gt=today, verb=verb)
            VideoCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb="G"+verb, object_set=notify)
        else:
            VideoCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=current_verb)
        community_send(list_id, community, None, socket_name)
    else:
        if VideoCommunityNotify.objects.filter(creator=creator, video_id=video_id, verb=current_verb).exists():
            pass
        elif VideoCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).exists():
            notify = VideoCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).last()
            VideoCommunityNotify.objects.create(creator=creator, community_id=community.id, video_id=video_id, verb=current_verb, user_set=notify)
        elif VideoCommunityNotify.objects.filter(community_id=community.id, created__gt=today, video_id=video_id, verb=verb).exists():
            notify = VideoCommunityNotify.objects.get(community_id=community.id, video_id=video_id, created__gt=today, verb=verb)
            VideoCommunityNotify.objects.create(creator=creator, community_id=community.id, video_id=video_id, verb="G"+verb, object_set=notify)
        else:
            VideoCommunityNotify.objects.create(creator=creator, community_id=community.id, video_id=video_id, verb=current_verb)
        community_send(video_id, community, None, socket_name)
