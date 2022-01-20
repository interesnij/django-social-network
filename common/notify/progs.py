from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def user_send_notify(id, creator_id, recipient_id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, recipient_id - id получателя, socket_name-имя, по которому следует назначать событие в скрипте js
    if creator_id != recipient_id:
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'notification',
            'id': str(id),
            'recipient_id': str(recipient_id),
            'name': socket_name,
        }
        async_to_sync(channel_layer.group_send)('notification', payload)

def community_send_notify(id, creator_id, recipient_id, community_id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, community_id-id сообщества, в которое шлется сокет,socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    if creator_id != recipient_id:
        payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': str(recipient_id),
            'community_id': str(community_id),
            'creator_community_id': str(action_community_id),
            'id': str(id),
            'name': socket_name,
        }
        async_to_sync(channel_layer.group_send)('notification', payload)


def user_send_wall(id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'community_id': str(action_community_id),
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

def community_send_wall(id, creator_id, community_id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, community_id-id сообщества, в которое шлется сокет,socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'community_id': str(community_id),
        'action_community_id': str(action_community_id),
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)
