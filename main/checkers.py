from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, AuthenticationFailed
from main.models import Item, ItemComment
from common.models import EmojiGroup



def check_can_update_post(user, item):
    check_has_post(user=user, item=item)
    if item.is_closed and item.community_id:
        if not user.is_staff_of_community_with_name(item.community.name):
            raise ValidationError(
                'Вы не можете редактировать закрытую запись',
            )


def check_comments_enabled_for_post_with_id(user, item_id):
    item = Item.objects.select_related('community').get(id=item_id)
    if item.community_id is not None:
        if not user.is_staff_of_community_with_name(item.community.name) and not item.comments_enabled:
            raise ValidationError(
                'Комментарии к этой записи отключены'
            )


def check_can_open_post_with_id(user, item_id):
    item = Item.objects.select_related('community').get(id=item_id)
    if item.community_id is None:
        raise ValidationError(
            'Только сообщения сообщества могут быть открыты / закрыты'
        )

    if not user.is_staff_of_community_with_name(item.community.name):
        raise ValidationError(
            'Только администраторы/модераторы могут открыть эту запись'
        )


def check_can_close_post(user, item):
    if item.community_id is None:
        raise ValidationError(
            'Только сообщения сообщества могут быть открыты / закрыты'
        )

    if not user.is_staff_of_community_with_name(item.community.name):
        raise ValidationError(
            'Только администраторы/модераторы могут закрыть эту запись'
        )


def check_can_delete_post(user, item):

    if not user.has_post(item=item):
        if Item.is_post_with_id_a_community_post(item.pk):
            if not user.is_moderator_of_community_with_name(
                    item.community.name) and not user.is_administrator_of_community_with_name(item.community.name):
                raise ValidationError(
                    'Только модераторы/администраторы могут удалять записи.',
                )
            else:
                item.community.create_remove_post_log(source_user=user,
                                                      target_user=item.creator)
        else:
            raise ValidationError(
                'Вы не можете удалить запись, которое вам не принадлежит'
            )


def check_can_mute_post(user, item):
    if user.has_muted_post_with_id(item_id=item.pk):
        raise ValidationError(
            'Запись уже не отправляет уведомления',
        )
    check_can_see_post(user=user, item=item)


def check_can_unmute_post(user, item):
    check_has_muted_post_with_id(item_id=item.pk, user=user)
    check_can_see_post(user=user, item=item)


def check_has_muted_post_with_id(user, item_id):
    if not user.has_muted_post_with_id(item_id=item_id):
        raise ValidationError(
            'Запись отправляет уведомления',
        )


def check_can_mute_post_comment(user, post_comment):
    if user.has_muted_post_comment_with_id(post_comment_id=post_comment.pk):
        raise ValidationError(
            'Комментарий к записи уже не отправляет уведомления',
        )

    check_can_see_post_comment(user=user, post_comment=post_comment)


def check_can_unmute_post_comment(user, post_comment):
    check_has_muted_post_comment_with_id(user=user, post_comment_id=post_comment.pk)
    check_can_see_post_comment(user=user, post_comment=post_comment)


def check_has_muted_post_comment_with_id(user, post_comment_id):
    if not user.has_muted_post_comment_with_id(post_comment_id=post_comment_id):
        raise ValidationError(
            'Комментарий к записи отправляет уведомления',
        )


def check_has_post(user, item):
    if not user.has_post(item=item):
        raise PermissionDenied(
            'Эта запись не принадлежит вам',
        )


def check_can_edit_comment_with_id_for_post(user, post_comment_id, item):
    check_can_see_post(user=user, item=item)

    if not ItemComment.objects.filter(id=post_comment_id, item_id=item.pk).exists():
        raise ValidationError(
            'Комментарий не относится к указанной записи'
        )

    if item.community and item.is_closed:
        is_administrator = user.is_administrator_of_community_with_name(item.community.name)
        is_moderator = user.is_moderator_of_community_with_name(item.community.name)
        if not is_moderator and not is_administrator:
            raise ValidationError(
                'Только администраторы/модераторы могут редактировать закрытый пост'
            )


def check_has_post_comment_with_id(user, post_comment_id):
    if not user.posts_comments.filter(id=post_comment_id).exists():
        raise ValidationError(
            'Вы не можете редактировать комментарий, который вам не принадлежит'
        )


def check_can_delete_comment_with_id_for_post(user, post_comment_id, item):
    check_can_see_post(user=user, item=item)

    if not ItemComment.objects.filter(id=post_comment_id, item_id=item.pk).exists():
        raise ValidationError(
            'Комментарий не относится к указанной записи'
        )
    is_comment_creator = user.posts_comments.filter(id=post_comment_id).exists()

    if item.community:
        is_moderator = user.is_moderator_of_community_with_name(item.community.name)
        is_administrator = user.is_administrator_of_community_with_name(item.community.name)
        if not is_administrator and not is_moderator:
            if item.is_closed:
                raise ValidationError(
                    'Только модераторы/администраторы могут удалять закрытые записи сообщества',
                )
            elif not is_comment_creator:
                raise ValidationError(
                    'Вы не можете удалить комментарий, который Вам не принадлежит'
                )
        else:
            post_comment = ItemComment.objects.select_related('commenter').get(pk=post_comment_id)
            if post_comment.parent_comment is not None:
                item.community.create_remove_post_comment_reply_log(source_user=user,
                                                                    target_user=post_comment.commenter)
            else:
                item.community.create_remove_post_comment_log(source_user=user,
                                                              target_user=post_comment.commenter)
    elif not item.creator_id == user.pk and not is_comment_creator:
        raise ValidationError(
            'Вы не можете удалить комментарий, который вам не принадлежит'
        )


def check_can_get_comments_for_post(user, item):
    check_can_see_post(user=user, item=item)


def check_can_get_comment_replies_for_post_and_comment(user, item, post_comment):
    if post_comment.item_id != item.id:
        raise ValidationError(
            'Комментарий с заданным идентификатором не найден'
        )
    check_can_see_post(user=user, item=post_comment.item)


def check_can_comment_in_post(user, item):
    check_can_see_post(user=user, item=item)
    check_comments_enabled_for_post_with_id(user=user, item_id=item.id)


def check_can_reply_to_post_comment_for_post(user, post_comment, item):
    if post_comment.item_id != item.id:
        raise ValidationError(
            'Комментарий с заданным идентификатором не найден'
        )

    check_can_comment_in_post(user=user, item=item)


def check_can_delete_reaction_with_id_for_post(user, post_reaction_id, item):
    check_can_see_post(user=user, item=item)
    if user.has_post(item=item):
        if not ItemReaction.objects.filter(id=post_reaction_id, item_id=item.pk).exists():
            raise ValidationError(
                'Эта реакция не относится к указанной записи'
            )
        return

    if not user.post_reactions.filter(id=post_reaction_id).exists():
        raise ValidationError(
            'Нельзя удалить реакцию, которая не принадлежит Вам.',
        )


def check_can_get_reactions_for_post(user, item):
    check_can_see_post(user=user, item=item)


def check_can_get_reactions_for_post_comment(user, post_comment):
    return check_can_get_reactions_for_post(user=user, item=post_comment.item)


def check_can_react_with_emoji_id(user, emoji_id):

    if not EmojiGroup.objects.filter(emojis__id=emoji_id, is_reaction_group=True).exists():
        raise ValidationError(
            'Этот смайл не действителен',
        )


def check_can_see_post(user, item):
    if not user.can_see_post(item):
        raise ValidationError(
            'Эта запись является частной.',
        )


def check_can_react_to_post_comment(user, post_comment, emoji_id):
    check_can_react_with_emoji_id(user=user, emoji_id=emoji_id)
    check_can_see_post_comment(user=user, post_comment=post_comment)

    if post_comment.item.is_closed:
        raise ValidationError(
            'Нельзя реагировать на комментарии к закрытой записи.',
        )


def check_can_delete_post_comment_reaction(user, post_comment_reaction):
    check_can_see_post_comment(user=user, post_comment=post_comment_reaction.post_comment)

    if post_comment_reaction.reactor_id != user.pk:
        raise ValidationError(
            'Нельзя удалить реакцию на комментарий, который Вам не пренадлежит.',
        )


def check_can_see_post_comment(user, post_comment):
    check_can_see_post(user=user, item=post_comment.post)

    if not user.can_see_post_comment(post_comment=post_comment):
        raise ValidationError(
            'Этот комментарий является частным',
        )


def check_can_get_comment_for_post(user, post_comment, item, ):
    check_can_see_post_comment(user=user, post_comment=post_comment)


def check_can_react_to_post(user, item):
    check_can_see_post(user=user, item=item)


def check_can_add_media_to_post(user, item):
    check_has_post(user=user, item=item)


def check_can_publish_post(user, item):
    check_has_post(user=user, item=item)


def check_can_get_status_for_post(user, item):
    check_has_post(user=user, item=item)


def check_can_get_media_for_post(user, item):
    check_can_see_post(user=user, item=item)


def check_can_get_preview_link_data_for_post(user, item):
    check_can_see_post(item=item, user=user)
    if not item.has_links():
        raise ValidationError(
            'Нет ссылки, связанной с записью.',
        )
