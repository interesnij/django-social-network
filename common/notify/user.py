from datetime import date
today = date.today()


def user_notify(creator, recipient_id, community_id, socket_name, verb):
    from notify.model.user import UserNotify

    current_verb = creator.get_verb_gender(verb)
    channel_layer = get_channel_layer()

    if community_id:
        if UserNotify.objects.filter(creator_id=creator.pk, community_id=community_id, verb=verb).exists():
            pass
        elif UserNotify.objects.filter(community_id=community_id, created__gt=today, verb=verb).exists():
            notify = UserNotify.objects.get(community_id=community_id, created__gt=today, verb=verb)
            UserNotify.objects.create(creator_id=creator.pk, community_id=community_id, verb="G"+verb, object_set=notify)
        else:
            PhotoNotify.objects.create(creator=creator, community_id=community_id, verb=verb)
        payload = {
            'type': 'receive',
            'key': 'notification',
            'community_id': community_id,
            'creator_id': creator.pk,
            'name': socket_name,
            }
    else:
        if UserNotify.objects.filter(creator_id=creator.pk, recipient_id=recipient_id, verb=verb).exists():
            pass
        elif UserNotify.objects.filter(recipient_id=recipient_id, created__gt=today, verb=verb).exists():
            notify = UserNotify.objects.get(recipient_id=recipient_id, created__gt=today, verb=verb)
            UserNotify.objects.create(creator_id=creator.pk, recipient_id=recipient_id, verb="G"+verb, object_set=notify)
        else:
            PhotoNotify.objects.create(creator=creator, recipient_id=recipient_id, verb=verb)
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient_id,
            'creator_id': creator.pk,
            'name': socket_name,
            }
    async_to_sync(channel_layer.group_send)('notification', payload)


def community_notify(creator, community, socket_name, verb):
    from notify.model.user import CommunityNotify

    current_verb = creator.get_verb_gender(verb)

    if CommunityNotify.objects.filter(creator_id=creator.pk, community_id=community_id, verb=verb).exists():
        pass
    elif CommunityNotify.objects.filter(community_id=community_id, created__gt=today, verb=verb).exists():
        notify = CommunityNotify.objects.get(community_id=community_id, created__gt=today, verb=verb)
        CommunityNotify.objects.create(creator_id=creator.pk, community_id=community_id, verb="G"+verb, object_set=notify)
    else:
        CommunityNotify.objects.create(creator_id=creator.pk, community_id=community_id, verb=verb)
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'recipient_id': recipient_id,
        'community_id': community.pk,
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)
