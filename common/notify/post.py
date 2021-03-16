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

def user_post_notify(creator, recipient_id, action_community_id, post_id, comment_id, list_id, socket_name, verb):
    from notify.model.post import PostNotify

    current_verb = creator.get_verb_gender(verb)
    if action_community_id:
        if PostNotify.objects.filter(community_id=action_community_id, post_id=post_id, verb=verb).exists():
            pass
        elif PostNotify.objects.filter(community_id=action_community_id, recipient_id=recipient_id, created__gt=today, verb=verb).exists():
            notify = PostNotify.objects.get(community_id=action_community_id, recipient_id=recipient_id, created__gt=today, verb=verb)
            PostNotify.objects.create(creator=creator, community_id=action_community_id, recipient_id=recipient_id, post_id=post_id, verb=verb, user_set=notify)
        elif PostNotify.objects.filter(recipient_id=recipient_id, community__isnull=False, post_id=post_id, created__gt=today, verb=verb).exists():
            notify = PostNotify.objects.get(recipient_id=recipient_id, community__isnull=False, post_id=post_id, created__gt=today, verb=verb)
            group_verb = "G" + verb
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, community_id=action_community_id, post_id=post_id, verb=group_verb, object_set=notify)
        else:
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, community_id=action_community_id, post_id=post_id, verb=verb)
        user_send(post_id, recipient_id, action_community_id, socket_name)
    elif comment_id:
        if PostNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif PostNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exists():
            notify = PostNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, verb=current_verb, user_set=notify)
        elif PostNotify.objects.filter(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb).exists():
            notify = PostNotify.objects.get(recipient_id=recipient_id, comment_id=comment_id, created__gt=today, verb=verb)
            group_verb = "G" + verb
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, comment_id=comment_id, verb=group_verb, object_set=notify)
        else:
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, comment_id=comment_id, verb=current_verb)
        user_send(comment_id, recipient_id, None, socket_name)
    elif list_id:
        if PostNotify.objects.filter(creator=creator, list_id=list_id, verb=current_verb).exists():
            pass
        elif PostNotify.objects.filter(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb).exists():
            notify = PostNotify.objects.get(creator=creator, recipient_id=recipient_id, created__gt=today, verb=current_verb)
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=current_verb, user_set=notify)
        elif PostNotify.objects.filter(recipient_id=recipient_id, list_id=list_id, created__gt=today, verb=verb).exists():
            notify = PostNotify.objects.get(recipient_id=recipient_id, list_id=list_id, created__gt=today, verb=verb)
            group_verb = "G" + verb
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=group_verb, object_set=notify)
        else:
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, list_id=list_id, verb=current_verb)
        user_send(list_id, recipient_id, None, socket_name)
    else:
        from django.db.models import Q
        if PostNotify.objects.filter(creator=creator, post_id=post_id, community__isnull=True, verb=current_verb).exists():
            pass
        elif PostNotify.objects.filter(creator=creator, recipient_id=recipient_id, community__isnull=True, created__gt=today, verb=current_verb).exists():
            notify = PostNotify.objects.filter(creator=creator, recipient_id=recipient_id, community__isnull=True, created__gt=today, verb=current_verb).last()
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, verb=current_verb, user_set=notify)
        elif PostNotify.objects.filter(Q(verb=verb)|Q(verb="W"+verb), recipient_id=recipient_id, community__isnull=True, created__gt=today, post_id=post_id).exists():
            notify = PostNotify.objects.get(Q(verb=verb)|Q(verb="W"+verb), recipient_id=recipient_id, community__isnull=True, post_id=post_id, created__gt=today)
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, verb="G"+verb, object_set=notify)
        else:
            PostNotify.objects.create(creator=creator, recipient_id=recipient_id, post_id=post_id, verb=current_verb)
        user_send(post_id, recipient_id, None, socket_name)

def community_post_notify(creator, community, action_community_id, post_id, comment_id, list_id, socket_name, verb):
    from notify.model.post import PostCommunityNotify

    current_verb = creator.get_verb_gender(verb)
    if action_community_id:
        if PostCommunityNotify.objects.filter(community_creator_id=action_community_id, post_id=post_id, verb=verb).exists():
            pass
        elif PostCommunityNotify.objects.filter(community_id=community.pk, community_creator_id=action_community_id, created__gt=today, verb=verb).exists():
            notify = PostCommunityNotify.objects.get(community_id=community.pk, community_creator_id=action_community_id, created__gt=today, verb=verb)
            PostCommunityNotify.objects.create(creator=creator, community_id=community.pk, community_creator_id=action_community_id, post_id=post_id, verb=verb, user_set=notify)
        elif PostCommunityNotify.objects.filter(community_id=community_id, post_id=post_id, created__gt=today, verb=verb).exists():
            notify = PostCommunityNotify.objects.get(community_id=community_id, post_id=post_id, created__gt=today, verb=verb)
            PostCommunityNotify.objects.create(creator=creator, community_creator_id=action_community_id, community_id=community.pk, post_id=post_id, verb="G" + verb, object_set=notify)
        else:
            PostCommunityNotify.objects.create(creator=creator, community_creator_id=action_community_id, community_id=community.pk, post_id=post_id, verb=verb)
        community_send(post_id, community, action_community_id, socket_name)
    elif comment_id:
        if PostCommunityNotify.objects.filter(creator=creator, comment_id=comment_id, verb=current_verb).exists():
            pass
        elif PostCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).exists():
            notify = PostCommunityNotify.objects.get(creator=creator, community_id=community.id, created__gt=today, verb=current_verb)
            PostCommunityNotify.objects.create(creator=creator, community_id=community.id, post_id=post_id, verb=current_verb, user_set=notify)
        elif PostCommunityNotify.objects.filter(community_id=community.id, comment_id=comment_id, created__gt=today, verb=verb).exists():
            notify = PostCommunityNotify.objects.get(community_id=community.id, comment_id=comment_id, created__gt=today, verb=verb)
            PostCommunityNotify.objects.create(creator=creator, community_id=community.id, post_id=post_id, comment_id=comment_id, verb="G" + verb, object_set=notify)
        else:
            PostCommunityNotify.objects.create(creator=creator, community_id=community.id, post_id=post_id, comment_id=comment_id, verb=current_verb)
        community_send(post_id, community, None, socket_name)
    elif list_id:
        if PostCommunityNotify.objects.filter(creator=creator, list_id=list_id, verb=current_verb).exists():
            pass
        elif PostCommunityNotify.objects.filter(creator=creator, community_id=community_id, created__gt=today, verb=current_verb).exists():
            notify = PostCommunityNotify.objects.get(creator=creator, community_id=community_id, created__gt=today, verb=current_verb)
            PostCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=current_verb, user_set=notify)
        elif PostCommunityNotify.objects.filter(community_id=community_id, list_id=list_id, created__gt=today, verb=verb).exists():
            notify = PostCommunityNotify.objects.get(community_id=community_id, list_id=list_id, created__gt=today, verb=verb)
            group_verb = "G" + verb
            PostCommunityNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=group_verb, object_set=notify)
        else:
            PostNotify.objects.create(creator=creator, community_id=community_id, list_id=list_id, verb=current_verb)
        community_send(list_id, community, None, socket_name)
    else:
        if PostCommunityNotify.objects.filter(creator=creator, post_id=post_id, verb=current_verb).exists():
            pass
        elif PostCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).exists():
            notify = PostCommunityNotify.objects.filter(creator=creator, community_id=community.id, created__gt=today, verb=current_verb).last()
            PostCommunityNotify.objects.create(creator=creator, community_id=community.id, post_id=post_id, verb=current_verb, user_set=notify)
        elif PostCommunityNotify.objects.filter(community_id=community.id, created__gt=today, post_id=post_id, verb=verb).exists():
            notify = PostCommunityNotify.objects.get(community_id=community.id, post_id=post_id, created__gt=today, verb=verb)
            PostCommunityNotify.objects.create(creator=creator, community_id=community.id, post_id=post_id, verb="G"+verb, object_set=notify)
        else:
            PostCommunityNotify.objects.create(creator=creator, community_id=community.id, post_id=post_id, verb=current_verb)
        community_send(post_id, community, None, socket_name)
