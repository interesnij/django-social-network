from django.conf import settings
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, AuthenticationFailed



def check_can_report_comment_for_post(user, post_comment, item):
    check_has_not_reported_post_comment_with_id(user=user, post_comment_id=post_comment.pk)
    check_can_see_post(user=user, item=item)

    if post_comment.commenter_id == user.pk:
        raise ValidationError(
            'Вы не можете создать репорт собственного комментария',
        )


def check_has_not_reported_post_comment_with_id(user, post_comment_id):
    if user.has_reported_post_comment_with_id(post_comment_id=post_comment_id):
        raise ValidationError(
            'Вы уже создали репорт о комментарии.',
        )


def check_can_report_post(user, item):
    check_can_see_post(user=user, item=item)
    check_has_not_reported_post_with_id(user=user, item_id=item.pk)
    if item.creator_id == user.pk:
        raise ValidationError(
            'Вы не можете создать репорт собственного сообщения',
        )


def check_has_not_reported_post_with_id(user, item_id):
    if user.has_reported_post_with_id(item_id=item_id):
        raise ValidationError(
            'Вы уже создали репорт о записи.',
        )


def check_can_report_user(user, user_to_report):
    check_has_not_reported_user_with_id(user=user, user_id=user_to_report.pk)
    if user.pk == user_to_report.pk:
        raise ValidationError(
            'Вы не можете создать репорт о себе...',
        )


def check_has_not_reported_user_with_id(user, user_id):
    if user.has_reported_user_with_id(user_id=user_id):
        raise ValidationError(
            'Вы уже создали репорт об этом пользователе',
        )


def check_can_report_community(user, community):
    check_has_not_reported_community_with_id(user=user, community_id=community.pk)
    if community.creator.pk == user.pk:
        raise ValidationError(
            'Вы не можете создать репорт о своем собственном сообществе',
        )


def check_has_not_reported_community_with_id(user, community_id):
    if user.has_reported_community_with_id(community_id=community_id):
        raise ValidationError(
            'Вы уже сообщили об этом сообществе',
        )


def check_can_get_global_moderated_objects(user):
    check_is_global_moderator(user=user)


def check_can_get_moderated_object(user, moderated_object):
    if user.is_global_moderator():
        return

    check_can_get_community_moderated_objects(user=user, community_name=moderated_object.community)


def check_can_get_community_moderated_objects(user, community_name):
    check_is_staff_of_community_with_name(user=user, community_name=community_name)


def check_has_not_reported_moderated_object_with_id(user, moderated_object_id):
    if user.has_reported_moderated_object_with_id(moderated_object_id=moderated_object_id):
        raise ValidationError(
            'Вы уже сообщили об объекте модерации',
        )


def check_can_update_moderated_object(user, moderated_object):
    check_can_moderate_moderated_object(user=user, moderated_object=moderated_object)

    if moderated_object.is_verified():
        raise PermissionDenied(
            'Модерируемый объект был проверен и больше не может редактироваться.'
        )

    if not moderated_object.is_pending() and not user.is_global_moderator():
        raise PermissionDenied(
            'Модерируемый объект уже утвержден / отклонен.'
        )


def check_can_approve_moderated_object(user, moderated_object):
    check_can_moderate_moderated_object(user=user, moderated_object=moderated_object)

    if moderated_object.is_verified():
        raise ValidationError(
            'Модерируемый объект уже проверен.'
        )


def check_can_reject_moderated_object(user, moderated_object):
    check_can_moderate_moderated_object(user=user, moderated_object=moderated_object)
    if moderated_object.is_verified():
        raise ValidationError(
            'Модерируемый объект уже проверен.'
        )


def check_can_unverify_moderated_object(user, moderated_object):
    check_is_global_moderator(user=user)
    if not moderated_object.is_verified():
        raise ValidationError(
            'Модерируемый объект не был проверен.'
        )


def check_can_verify_moderated_object(user, moderated_object):
    check_is_global_moderator(user=user)
    if moderated_object.is_verified():
        raise ValidationError(
            'Модерируемый объект уже проверен.'
        )

    if moderated_object.is_pending():
        raise ValidationError(
            'Вы не можете проверить управляемый объект со статусом ожидание. Пожалуйста, одобрите или отклоните его.'
        )


def check_can_moderate_moderated_object(user, moderated_object):
    content_object = moderated_object.content_object

    is_global_moderator = user.is_global_moderator()

    if is_global_moderator:
        return

    if isinstance(content_object, Item):
        if content_object.community:
            if not user.is_staff_of_community_with_name(community_name=content_object.community.name):
                raise ValidationError('Только сотрудники сообщества могут модерировать сообщения сообщества')
        else:
            raise ValidationError('Только глобальные модераторы могут модерировать сообщения, не относящиеся к сообществу')
    elif isinstance(content_object, PostComment):
        if content_object.item.community:
            if not user.is_staff_of_community_with_name(community_name=content_object.item.community.name):
                raise ValidationError('Только сотрудники сообщества могут модерировать комментарии к публикациям сообщества')
        else:
            raise ValidationError('Только глобальные модераторы могут модерировать комментарии, не относящиеся к сообществу')
    else:
        raise ValidationError('Не глобальные модераторы могут только модерировать записи и комментарии.')


def check_is_global_moderator(user):
    if not user.is_global_moderator():
        raise PermissionDenied('Не глобальный модератор.')
