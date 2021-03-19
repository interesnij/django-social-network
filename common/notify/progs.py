from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def user_send(id, recipient_id, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, recipient_id - id получателя, socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'recipient_id': recipient_id,
        'community_id': action_community_id,
        'id': str(id),
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

def community_send(id, creator_id, community, action_community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, community_id-id сообщества, в которое шлется сокет,socket_name-имя, по которому следует назначать событие в скрипте js
    persons = community.get_staff_members()
    channel_layer = get_channel_layer()
    for user in persons:
        if creator_id != user.pk:
            payload = {
                'type': 'receive',
                'key': 'notification',
                'recipient_id': user.pk,
                'community_id': community.pk,
                'creator_community_id': action_community_id,
                'id':  id,
                'name': socket_name,
            }
    async_to_sync(channel_layer.group_send)('notification', payload)
