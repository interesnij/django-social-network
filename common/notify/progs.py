from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def user_send_notify(id, recipient_id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, recipient_id - id получателя, socket_name-имя, по которому следует назначать событие в скрипте js
    user_ids, channel_layer = community.get_member_for_notify_ids(), get_channel_layer()
    for user_id in user_ids:
        Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, attach="pos"+str(post.pk), verb="ITE")
        payload = {
            'type': 'receive',
            'key': 'notification',
            'id': str(post.pk),
            'recipient_id': str(user_id),
            'name': "u_post_create",
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

def community_send_notify(id, creator_id, community, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, community_id-id сообщества, в которое шлется сокет,socket_name-имя, по которому следует назначать событие в скрипте js
    user_ids, channel_layer = community.get_member_for_notify_ids(), get_channel_layer()
    for user_id in user_ids:
        if creator_id != user_id:
            payload = {
                'type': 'receive',
                'key': 'notification',
                'recipient_id': user_id,
                'community_id': community.pk,
                'creator_community_id': action_community_id,
                'id': id,
                'name': socket_name,
            }
            async_to_sync(channel_layer.group_send)('notification', payload)


def user_send_wall(id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'community_id': action_community_id,
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

def community_send_wall(id, creator_id, community, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, community_id-id сообщества, в которое шлется сокет,socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'community_id': community.pk,
        'action_community_id': action_community_id,
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)
