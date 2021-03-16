from datetime import date
today = date.today()
from common.notify.progs import *


def user_good_notify(creator, recipient_id, action_community_id, good_id, comment_id, list_id, socket_name, verb):
    from notify.model.good import GoodNotify

    current_verb = creator.get_verb_gender(verb)
    if action_community_id:
        if GoodNotify.objects.filter(community_id=action_community_id, good_id=good_id, verb=verb).exists():
            pass
        elif GoodNotify.objects.filter(community_id=action_community_id, recipient_id=recipient_id, created__gt=today, verb=verb).exists():
            notify = GoodNotify.objects.get(community_id=action_community_id, recipient_id=recipient_id, created__gt=today, verb=verb)
            GoodNotify.objects.create(creator=creator, community_id=action_community_id, recipient_id=recipient_id, good_id=good_id, verb=verb, user_set=notify)
        elif GoodNotify.objects.filter(recipient_id=recipient_id, community__isnull=False, good_id=good_id, created__gt=today, verb=verb).exists():
            notify = GoodNotify.objects.get(recipient_id=recipient_id, community__isnull=False, good_id=good_id, created__gt=today, verb=verb)
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, community_id=action_community_id, good_id=good_id, verb="G"+verb, object_set=notify)
        else:
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, community_id=action_community_id, good_id=good_id, verb=verb)
        user_send(good_id, recipient_id, action_community_id, socket_name)
    elif comment_id:
        if GoodNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif GoodNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exists():
            notify = GoodNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, good_id=good_id, verb=current_verb, user_set=notify)
        elif GoodNotify.objects.filter(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb).exists():
            notify = GoodNotify.objects.get(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb)
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, good_id=good_id, comment_id=comment_id, verb="G"+verb, object_set=notify)
        else:
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, good_id=good_id, comment_id=comment_id, verb=current_verb)
        user_send(comment_id, recipient_id, None, socket_name)
    elif list_id:
        if GoodNotify.objects.filter(creator=creator, list_id=list_id, verb=current_verb).exists():
            pass
        elif GoodNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exists():
            notify = GoodNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=current_verb, user_set=notify)
        elif GoodNotify.objects.filter(recipient_id=recipient_id, list_id=list_id, created__gt=today, verb=verb).exists():
            notify = GoodNotify.objects.get(recipient_id=recipient_id, list_id=list_id, created__gt=today, verb=verb)
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb="G"+verb, object_set=notify)
        else:
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=current_verb)
        user_send(list_id, recipient_id, None, socket_name)
    else:
        from django.db.models import Q
        if GoodNotify.objects.filter(creator=creator, good_id=good_id, community__isnull=True, verb=current_verb).exists():
            pass
        elif GoodNotify.objects.filter(creator=creator, recipient_id=recipient_id, community__isnull=True, created__gt=today, verb=current_verb).exists():
            notify = GoodNotify.objects.filter(creator=creator, recipient_id=recipient_id, community__isnull=True, created__gt=today, verb=current_verb).last()
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, good_id=good_id, verb=current_verb, user_set=notify)
        elif GoodNotify.objects.filter(Q(verb=verb)|Q(verb="W"+verb), recipient_id=recipient_id, community__isnull=True, created__gt=today, good_id=good_id).exists():
            notify = GoodNotify.objects.get(Q(verb=verb)|Q(verb="W"+verb), recipient_id=recipient_id, community__isnull=True, good_id=good_id, created__gt=today)
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, good_id=good_id, verb="G"+verb, object_set=notify)
        else:
            GoodNotify.objects.create(creator=creator, recipient_id=recipient_id, good_id=good_id, verb=current_verb)
        user_send(good_id, recipient_id, None, socket_name)

def community_good_notify(creator, community, action_community_id, good_id, comment_id, list_id, socket_name, verb):
    from notify.model.good import GoodCommunityNotify

    current_verb = creator.get_verb_gender(verb)
    if action_community_id:
        if GoodCommunityNotify.objects.filter(community_creator_id=action_community_id, good_id=good_id, verb=verb).exists():
            pass
        elif GoodCommunityNotify.objects.filter(community_id=community.pk, community_creator_id=action_community_id, created__gt=today, verb=verb).exists():
            notify = GoodCommunityNotify.objects.get(community_id=community.pk, community_creator_id=action_community_id, created__gt=today, verb=verb)
            GoodCommunityNotify.objects.create(creator=creator, community_id=community.pk, community_creator_id=action_community_id, good_id=good_id, verb=verb, user_set=notify)
        elif GoodCommunityNotify.objects.filter(community_id=community_id, good_id=good_id, created__gt=today, verb=verb).exists():
            notify = GoodCommunityNotify.objects.get(community_id=community_id, good_id=good_id, created__gt=today, verb=verb)
            GoodCommunityNotify.objects.create(creator=creator, community_creator_id=action_community_id, community_id=community.pk, good_id=good_id, verb="G"+verb, object_set=notify)
        else:
            GoodCommunityNotify.objects.create(creator=creator, community_creator_id=action_community_id, community_id=community.pk, good_id=good_id, verb=verb)
        community_send(good_id, community, action_community_id, socket_name)
    elif comment_id:
        if GoodCommunityNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif GoodCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).exists():
            notify = GoodCommunityNotify.objects.get(creator=creator, community_id=community.id, created__gt=today, verb=current_verb)
            GoodCommunityNotify.objects.create(creator=creator, community_id=community.id, good_id=good_id, verb=current_verb, user_set=notify)
        elif GoodCommunityNotify.objects.filter(community_id=community.id, comment_id=comment_id, created__gt=today, verb=verb).exists():
            notify = GoodCommunityNotify.objects.get(community_id=community.id, comment_id=comment_id, created__gt=today, verb=verb)
            GoodCommunityNotify.objects.create(creator=creator, community_id=community.id, good_id=good_id, comment_id=comment_id, verb="G"+verb, object_set=notify)
        else:
            GoodCommunityNotify.objects.create(creator=creator, community_id=community.id, good_id=good_id, comment_id=comment_id, verb=current_verb)
        community_send(comment_id, community, None, socket_name)
    elif list_id:
        if GoodCommunityNotify.objects.filter(creator=creator, list_id=list_id, verb=current_verb).exists():
            pass
        elif GoodCommunityNotify.objects.filter(creator=creator, community_id=community_id, created__gt=today, verb=current_verb).exists():
            notify = GoodCommunityNotify.objects.get(creator=creator, community_id=community_id, created__gt=today, verb=current_verb)
            GoodCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=current_verb, user_set=notify)
        elif GoodCommunityNotify.objects.filter(community_id=community_id, list_id=list_id, created__gt=today, verb=verb).exists():
            notify = GoodCommunityNotify.objects.get(community_id=community_id, list_id=list_id, created__gt=today, verb=verb)
            GoodCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb="G"+verb, object_set=notify)
        else:
            GoodCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=current_verb)
        community_send(list_id, community, None, socket_name)
    else:
        if GoodCommunityNotify.objects.filter(creator=creator, good_id=good_id, verb=current_verb).exists():
            pass
        elif GoodCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).exists():
            notify = GoodCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).last()
            GoodCommunityNotify.objects.create(creator=creator, community_id=community.id, good_id=good_id, verb=current_verb, user_set=notify)
        elif GoodCommunityNotify.objects.filter(community_id=community.id, created__gt=today, good_id=good_id, verb=verb).exists():
            notify = GoodCommunityNotify.objects.get(community_id=community.id, good_id=good_id, created__gt=today, verb=verb)
            GoodCommunityNotify.objects.create(creator=creator, community_id=community.id, good_id=good_id, verb="G"+verb, object_set=notify)
        else:
            GoodCommunityNotify.objects.create(creator=creator, community_id=community.id, good_id=good_id, verb=current_verb)
        community_send(good_id, community, None, socket_name)
