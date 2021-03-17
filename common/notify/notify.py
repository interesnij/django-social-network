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

    if Notify.objects.filter(creator_id=creator_id, action_community_id=action_community_id, recipient_id=recipient_id, attach=attach, verb=verb).exists():
        pass
    elif Notify.objects.filter(recipient_id=recipient_id, action_community_id=action_community_id, created__gt=today, attach__in=attach[:3], verb=verb).exists():
        notify = Notify.objects.get(recipient_id=recipient_id, action_community_id=action_community_id, attach=attach, created__gt=today, verb=verb)
        Notify.objects.create(creator=creator, action_community_id=action_community_id, recipient_id=recipient_id, attach=attach, verb=verb, user_set=notify)
    elif Notify.objects.filter(recipient_id=recipient_id, action_community_id=action_community_id, post_id=post_id, created__gt=today, verb=verb).exists():
        notify = Notify.objects.get(recipient_id=recipient_id, action_community_id=action_community_id, attach=attach, created__gt=today, verb=verb)
        Notify.objects.create(creator=creator, recipient_id=recipient_id, action_community_id=action_community_id, attach=attach, verb="G"+verb, object_set=notify)
    else:
        Notify.objects.create(creator=creator, recipient_id=recipient_id, action_community_id=action_community_id, attach=attach, verb=verb)
    user_send(attach[3:], recipient_id, action_community_id, socket_name)

def community_notify(creator, community, action_community_id, attach, socket_name, verb):
    from notify.model.post import Notify

    current_verb = creator.get_verb_gender(verb)

    if Notify.objects.filter(creator_id=creator_id, community_id=community_id, action_community_id=action_community_id, attach=attach, verb=verb).exists():
        pass
    elif Notify.objects.filter(creator_id=creator_id, community_id=community.pk, action_community_id=action_community_id, created__gt=today, attach__in=attach[:3], verb=verb).exists():
        notify = Notify.objects.get(creator_id=creator_id, community_id=community.pk, created__gt=today, action_community_id=action_community_id, attach=attach, verb=verb)
        Notify.objects.create(creator_id=creator_id, community_id=community.pk, action_community_id=action_community_id, attach=attach, verb=verb, user_set=notify)
    elif Notify.objects.filter(community_id=community_id, attach=attach, created__gt=today, verb=verb).exists():
        notify = Notify.objects.get(community_id=community_id, attach=attach, created__gt=today, verb=verb)
        Notify.objects.create(creator_id=creator_id, action_community_id=action_community_id, community_id=community.pk, attach=attach, verb="G"+verb, object_set=notify)
    else:
        Notify.objects.create(creator_id=creator_id, action_community_id=action_community_id, community_id=community.pk, attach=attach, verb=verb)
    community_send(attach[3:], community, action_community_id, socket_name)
