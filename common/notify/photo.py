from datetime import date
today = date.today()
from common.notify.progs import *


def user_photo_notify(creator, recipient_id, action_community_id, photo_id, comment_id, list_id, socket_name, verb):
    from notify.model.photo import PhotoNotify

    current_verb = creator.get_verb_gender(verb)
    if action_community_id:
        if PhotoNotify.objects.filter(community_id=action_community_id, photo_id=photo_id, verb=verb).exists():
            pass
        elif PhotoNotify.objects.filter(community_id=action_community_id, recipient_id=recipient_id, created__gt=today, verb=verb).exists():
            notify = PhotoNotify.objects.get(community_id=action_community_id, recipient_id=recipient_id, created__gt=today, verb=verb)
            PhotoNotify.objects.create(creator=creator, community_id=action_community_id, recipient_id=recipient_id, photo_id=photo_id, verb=verb, user_set=notify)
        elif PhotoNotify.objects.filter(recipient_id=recipient_id, community__isnull=False, photo_id=photo_id, created__gt=today, verb=verb).exists():
            notify = PhotoNotify.objects.get(recipient_id=recipient_id, community__isnull=False, photo_id=photo_id, created__gt=today, verb=verb)
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, community_id=action_community_id, photo_id=photo_id, verb="G"+verb, object_set=notify)
        else:
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, community_id=action_community_id, photo_id=photo_id, verb=verb)
        user_send(photo_id, recipient_id, action_community_id, socket_name)
    elif comment_id:
        if PhotoNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif PhotoNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exists():
            notify = PhotoNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, photo_id=photo_id, verb=current_verb, user_set=notify)
        elif PhotoNotify.objects.filter(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb).exists():
            notify = PhotoNotify.objects.get(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb)
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, photo_id=photo_id, comment_id=comment_id, verb="G"+verb, object_set=notify)
        else:
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, photo_id=photo_id, comment_id=comment_id, verb=current_verb)
        user_send(comment_id, recipient_id, None, socket_name)
    elif list_id:
        if PhotoNotify.objects.filter(creator=creator, list_id=list_id, verb=current_verb).exists():
            pass
        elif PhotoNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exists():
            notify = PhotoNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=current_verb, user_set=notify)
        elif PhotoNotify.objects.filter(recipient_id=recipient_id, list_id=list_id, created__gt=today, verb=verb).exists():
            notify = PhotoNotify.objects.get(recipient_id=recipient_id, list_id=list_id, created__gt=today, verb=verb)
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb="G"+verb, object_set=notify)
        else:
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=current_verb)
        user_send(list_id, recipient_id, None, socket_name)
    else:
        from django.db.models import Q
        if PhotoNotify.objects.filter(creator=creator, photo_id=photo_id, community__isnull=True, verb=current_verb).exists():
            pass
        elif PhotoNotify.objects.filter(creator=creator, recipient_id=recipient_id, community__isnull=True, created__gt=today, verb=current_verb).exists():
            notify = PhotoNotify.objects.filter(creator=creator, recipient_id=recipient_id, community__isnull=True, created__gt=today, verb=current_verb).last()
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, photo_id=photo_id, verb=current_verb, user_set=notify)
        elif PhotoNotify.objects.filter(Q(verb=verb)|Q(verb="W"+verb), recipient_id=recipient_id, community__isnull=True, created__gt=today, photo_id=photo_id).exists():
            notify = PhotoNotify.objects.get(Q(verb=verb)|Q(verb="W"+verb), recipient_id=recipient_id, community__isnull=True, photo_id=photo_id, created__gt=today)
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, photo_id=photo_id, verb="G"+verb, object_set=notify)
        else:
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, photo_id=photo_id, verb=current_verb)
        user_send(photo_id, recipient_id, None, socket_name)

def community_photo_notify(creator, community, action_community_id, photo_id, comment_id, list_id, socket_name, verb):
    from notify.model.photo import PhotoCommunityNotify

    current_verb = creator.get_verb_gender(verb)
    if action_community_id:
        if PhotoCommunityNotify.objects.filter(community_creator_id=action_community_id, photo_id=photo_id, verb=verb).exists():
            pass
        elif PhotoCommunityNotify.objects.filter(community_id=community.pk, community_creator_id=action_community_id, created__gt=today, verb=verb).exists():
            notify = PhotoCommunityNotify.objects.get(community_id=community.pk, community_creator_id=action_community_id, created__gt=today, verb=verb)
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community.pk, community_creator_id=action_community_id, photo_id=photo_id, verb=verb, user_set=notify)
        elif PhotoCommunityNotify.objects.filter(community_id=community_id, photo_id=photo_id, created__gt=today, verb=verb).exists():
            notify = PhotoCommunityNotify.objects.get(community_id=community_id, photo_id=photo_id, created__gt=today, verb=verb)
            PhotoCommunityNotify.objects.create(creator=creator, community_creator_id=action_community_id, community_id=community.pk, photo_id=photo_id, verb="G"+verb, object_set=notify)
        else:
            PhotoCommunityNotify.objects.create(creator=creator, community_creator_id=action_community_id, community_id=community.pk, photo_id=photo_id, verb=verb)
        community_send(photo_id, community, action_community_id, socket_name)
    elif comment_id:
        if PhotoCommunityNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif PhotoCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).exists():
            notify = PhotoCommunityNotify.objects.get(creator=creator, community_id=community.id, created__gt=today, verb=current_verb)
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community.id, photo_id=photo_id, verb=current_verb, user_set=notify)
        elif PhotoCommunityNotify.objects.filter(community_id=community.id, comment_id=comment_id, created__gt=today, verb=verb).exists():
            notify = PhotoCommunityNotify.objects.get(community_id=community.id, comment_id=comment_id, created__gt=today, verb=verb)
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community.id, photo_id=photo_id, comment_id=comment_id, verb="G"+verb, object_set=notify)
        else:
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community.id, photo_id=photo_id, comment_id=comment_id, verb=current_verb)
        community_send(comment_id, community, None, socket_name)
    elif list_id:
        if PhotoCommunityNotify.objects.filter(creator=creator, list_id=list_id, verb=current_verb).exists():
            pass
        elif PhotoCommunityNotify.objects.filter(creator=creator, community_id=community_id, created__gt=today, verb=current_verb).exists():
            notify = PhotoCommunityNotify.objects.get(creator=creator, community_id=community_id, created__gt=today, verb=current_verb)
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=current_verb, user_set=notify)
        elif PhotoCommunityNotify.objects.filter(community_id=community_id, list_id=list_id, created__gt=today, verb=verb).exists():
            notify = PhotoCommunityNotify.objects.get(community_id=community_id, list_id=list_id, created__gt=today, verb=verb)
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb="G"+verb, object_set=notify)
        else:
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=current_verb)
        community_send(list_id, community, None, socket_name)
    else:
        if PhotoCommunityNotify.objects.filter(creator=creator, photo_id=photo_id, verb=current_verb).exists():
            pass
        elif PhotoCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).exists():
            notify = PhotoCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).last()
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community.id, photo_id=photo_id, verb=current_verb, user_set=notify)
        elif PhotoCommunityNotify.objects.filter(community_id=community.id, created__gt=today, photo_id=photo_id, verb=verb).exists():
            notify = PhotoCommunityNotify.objects.get(community_id=community.id, photo_id=photo_id, created__gt=today, verb=verb)
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community.id, photo_id=photo_id, verb="G"+verb, object_set=notify)
        else:
            PhotoCommunityNotify.objects.create(creator=creator, community_id=community.id, photo_id=photo_id, verb=current_verb)
        community_send(photo_id, community, None, socket_name)
