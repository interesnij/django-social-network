from datetime import date
today = date.today()
from common.notify.progs import *

""" Сохранение уведомления о событиях записей. - user_post_notify, community_post_notify
    Мы создаём группы уведомлений по сегодняшнему дню, исключая случаи, когда creator != recipient:
    1. Если пользователь уже делал "тип уведомления", то запись не создается
    2. Фильтруем записи уведомлений постов. Если есть запись, которую создал
        creator, а получатель её recipient, и verb совпадает с verb этой записи, значит создаём новую запись с прикреплением её
        к найденной записи. Это пример уведомлений "Тот-то оценил 2 Ваши записи".
    3. Если записи нет, тогда снова ищем, но только по совпадению "получатель её recipient, id объекта post_id
        и verb совпадает с verb" за сегодняший день. Если запись есть, то создаем новую и прицепляем к ней.
        Это пример уведомлений "Тот-то и тот-то оценили пост" или "Тот-то и ещё 7 человек оценили пост".
    4. Если ни той, ни той записи нет, тогда просто создаем новую запись. Пример уведомлений
        "Тот-то оценил Ваш пост".
"""

def user_notify(creator, recipient_id, action_community_id, attach, socket_name, verb):
    from notify.models import Notify

    current_verb = creator.get_verb_gender(verb)

    if Notify.objects.filter(creator_id=creator.pk, action_community_id=action_community_id, recipient_id=recipient_id, attach=attach, verb=verb).exists():
        pass
    elif Notify.objects.filter(recipient_id=recipient_id, action_community_id=action_community_id, created__gt=today, attach__contains=attach[:3], verb=current_verb).exists():
        notify = Notify.objects.get(recipient_id=recipient_id, action_community_id=action_community_id, attach__contains=attach[:3], created__gt=today, verb=current_verb)
        Notify.objects.create(creator_id=creator.pk, action_community_id=action_community_id, recipient_id=recipient_id, attach=attach, verb=current_verb, user_set=notify)
    elif Notify.objects.filter(recipient_id=recipient_id, attach=attach, created__gt=today, verb=verb).exists():
        notify = Notify.objects.get(recipient_id=recipient_id, attach=attach, created__gt=today, verb=verb)
        Notify.objects.create(creator_id=creator.pk, recipient_id=recipient_id, action_community_id=action_community_id, attach=attach, verb="G"+verb, object_set=notify)
    else:
        Notify.objects.create(creator_id=creator.pk, recipient_id=recipient_id, action_community_id=action_community_id, attach=attach, verb=current_verb)
    user_send_notify(attach[3:], recipient_id, action_community_id, socket_name)

def community_notify(creator, community, action_community_id, attach, socket_name, verb):
    from notify.models import Notify

    current_verb = creator.get_verb_gender(verb)

    if Notify.objects.filter(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, attach=attach, verb=verb).exists():
        pass
    elif Notify.objects.filter(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, created__gt=today, attach__in=attach[:3], verb=verb).exists():
        notify = Notify.objects.get(creator_id=creator.pk, community_id=community.pk, created__gt=today, action_community_id=action_community_id, attach=attach, verb=verb)
        Notify.objects.create(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, attach=attach, verb=verb, user_set=notify)
    elif Notify.objects.filter(community_id=community.pk, attach=attach, created__gt=today, verb=verb).exists():
        notify = Notify.objects.get(community_id=community.pk, attach=attach, created__gt=today, verb=verb)
        Notify.objects.create(creator_id=creator.pk, action_community_id=action_community_id, community_id=community.pk, attach=attach, verb="G"+verb, object_set=notify)
    else:
        Notify.objects.create(creator_id=creator.pk, action_community_id=action_community_id, community_id=community.pk, attach=attach, verb=current_verb)
    community_send_notify(attach[3:], creator.pk, community, action_community_id, socket_name)


def user_wall(creator, action_community_id, attach, socket_name, verb):
    from notify.models import Wall

    current_verb = creator.get_verb_gender(verb)

    if Wall.objects.filter(creator_id=creator.pk, action_community_id=action_community_id, attach=attach, verb=verb).exists():
        pass
    #elif Wall.objects.filter(action_community_id=action_community_id, created__gt=today, attach__contains=attach[:3], verb=current_verb).exists():
    #    notify = Wall.objects.get(action_community_id=action_community_id, attach__contains=attach[:3], created__gt=today, verb=current_verb)
    #    Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, attach=attach, verb=current_verb, user_set=notify)
    elif Wall.objects.filter(attach=attach, created__gt=today, verb=verb).exists():
        notify = Wall.objects.get(attach=attach, created__gt=today, verb=verb)
        Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, attach=attach, verb="G"+verb, object_set=notify)
    else:
        Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, attach=attach, verb=current_verb)
    user_send_wall(attach[3:], action_community_id, socket_name)

def community_wall(creator, community, action_community_id, attach, socket_name, verb):
    from notify.models import Wall

    current_verb = creator.get_verb_gender(verb)

    if Wall.objects.filter(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, attach=attach, verb=verb).exists():
        pass
    #elif Wall.objects.filter(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, created__gt=today, attach__in=attach[:3], verb=verb).exists():
    #    notify = Wall.objects.get(creator_id=creator.pk, community_id=community.pk, created__gt=today, action_community_id=action_community_id, attach=attach, verb=verb)
    #    Wall.objects.create(creator_id=creator.pk, community_id=community.pk, action_community_id=action_community_id, attach=attach, verb=verb, user_set=notify)
    elif Wall.objects.filter(community_id=community.pk, attach=attach, created__gt=today, verb=verb).exists():
        notify = Wall.objects.get(community_id=community.pk, attach=attach, created__gt=today, verb=verb)
        Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, community_id=community.pk, attach=attach, verb="G"+verb, object_set=notify)
    else:
        Wall.objects.create(creator_id=creator.pk, action_community_id=action_community_id, community_id=community.pk, attach=attach, verb=current_verb)
    community_send_wall(attach[3:], creator.pk, community, action_community_id, socket_name)
