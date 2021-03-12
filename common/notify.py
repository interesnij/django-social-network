from datetime import date
today = date.today()
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def user_send(id, recipient_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
            'type': 'receive',
            'key': 'notification',
            'recipient_id': recipient_id,
            'id': str(id),
            'name': socket_name,
        }
    async_to_sync(channel_layer.group_send)('notification', payload)

def community_send(id, community_id, socket_name):
    # посылаем сокет с переменными: id-id объекта, community_id-id сообщества, в которое шлется сокет,socket_name-имя, по которому следует назначать событие в скрипте js
    channel_layer = get_channel_layer()
    payload = {
        'type': 'receive',
        'key': 'notification',
        'recipient_id': user.pk,
        'community_id': community_id,
        'id':  id,
        'name': socket_name,
    }
    async_to_sync(channel_layer.group_send)('notification', payload)

"""
    скрипт посылки уведомления, решающий все вопросы и все нюансы.
    1. Переменные...
    1.1 creator - создатель уведомления, инициатор
    1.2 recipient_id - получатель уведомления, владелец или админ
    1.3 item_id - объект
    1.4 comment_id - коммент
    1.5 action_community - сообщество, которое поделилилось записью пользователя или сообщества
    1.6 community - сообщество - получатель уведомления
    1.7 socket_name - название сокета для отлавливания в скрипте js.
    1.8 verb - Тип уведомления, который мы проверим на пол инициатора и на множественное число.

    2. Схема перебора моделей...
    2.1 Сначала обработаем репосты (action_community)
    2.2 Затем разделим на пользователя и сообщество, а там на комменты и объекты
    2.3 Оставшиеся варианты переберем по socket_name.

"""
def item_notification_handler(creator,
                                recipient_id,
                                item_id,
                                comment_id,
                                action_community,
                                community,
                                socket_name,
                                verb):
    if action_community:
        return "Обрабатываем репосты"
    elif community:
        if comment_id:
            return "Обрабатываем комменты сообществ"
        else:
            return "Обрабатываем объекты сообществ"
    else:
        if socket_name == "u_post_comment_notify":
            save_post_notify(creator, recipient_id, item_id, comment_id, verb)
            user_send(comment_id, recipient_id, socket_name)
        else:
            if socket_name == "u_post_notify":
                save_post_notify(creator, recipient_id, item_id, None, verb)
                user_send(item_id, recipient_id, socket_name)


def save_post_notify(creator, recipient_id, post_id, comment_id, verb):
    from notify.model.post import PostNotify
    """ Сохранение уведомления о событиях записей пользователя.
        Мы создаём группы уведомлений по сегодняшнему дню, исключая случаи, когда creator != recipient:
        1. По сегодняшнему дню фильтруем записи уведомлений постов. Если есть запись, которую создал
        creator, а получатель её recipient, и verb совпадает с verb этой записи, значит создаём новую запись с прикреплением её
        к найденной записи. Это пример уведомлений "Тот-то оценил 2 Ваши записи".
        2. Если записи нет, тогда снова ищем, но только по совпадению "получатель её recipient, и verb совпадает с verb" за
        сегодняший день. Если запись есть, то создаем новую и прицепляем к ней. Это пример уведомлений
        "Тот-то и тот-то оценили пост" или "Тот-то и ещё 7 человек оценили пост".
        3. Если ни той, ни той записи нет, тогда просто создаем новую запись. Пример уведомлений
        "Тот-то оценил Ваш пост".
    """
    current_verb = creator.get_verb_gender(verb)
    if comment_id:
        if PostNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif PostNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exclude(creator_id=recipient_id).exists():
            notify = PostNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, verb=current_verb, object_set=notify)
        elif PostNotify.objects.filter(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb).exclude(creator_id=recipient_id).exists():
            notify = PostNotify.objects.get(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb)
            group_verb = "G" + verb
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, comment_id=comment_id, verb=group_verb, user_set=notify)
        else:
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, comment_id=comment_id, verb=current_verb)
    else:
        if PostNotify.objects.filter(creator=creator, post_id=post_id, verb=current_verb).exists():
            pass
        elif PostNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exclude(creator_id=recipient_id).exists():
            notify = PostNotify.objects.get(creator=creator, recipient_id=recipient_id, post_id=post_id, created__gt=today, verb=current_verb)
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, verb=verb, object_set=notify)
        elif PostNotify.objects.filter(recipient_id=recipient_id, created__gt=today, post_id=post_id, verb=verb).exclude(creator_id=recipient_id).exists():
            notify = PostNotify.objects.get(recipient_id=recipient_id, post_id=post_id, created__gt=today, verb=verb)
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, verb="G"+verb, user_set=notify)
        else:
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, verb=current_verb)
