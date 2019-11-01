from rest_framework.exceptions import ValidationError, PermissionDenied
from communities.models import Community



def check_can_post_to_community_with_name(user, community_name=None):
    if not user.is_member_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Вы не можете публиковать записи в сообществе, членом которого Вы не являетесь',
        )


def check_can_enable_disable_comments_for_post_in_community_with_name(user, community_name):
    if not user.is_moderator_of_community_with_name(community_name) and \
            not user.is_administrator_of_community_with_name(community_name):
        raise ValidationError(
            'Только администраторы / модераторы могут включать / выключать комментарии к записи сообщества',
        )


def check_can_delete_community_with_name(user, community_name):
    if not user.is_creator_of_community_with_name(community_name):
        raise ValidationError(
            'Не удается удалить сообщество, которое вы не администрируете.',
        )


def check_can_update_community_with_name(user, community_name):
    if not user.is_administrator_of_community_with_name(community_name):
        raise ValidationError(
            'Не удается обновить сообщество, которое вы не администрируете.',
        )


def check_can_get_posts_for_community_with_name(user, community_name):
    check_is_not_banned_from_community_with_name(user=user, community_name=community_name)
    if Community.is_community_with_name_private(
            community_name=community_name) and not user.is_member_of_community_with_name(
        community_name=community_name):
        raise ValidationError(
            'Сообщество является частным. Вы должны стать участником, чтобы видеть его записи.',
        )


def check_can_get_closed_posts_for_community_with_name(user, community_name):
    if not user.is_administrator_of_community_with_name(community_name=community_name) and \
            not user.is_moderator_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Только администраторы/модераторы могут просматривать закрытые записи',
        )


def check_can_get_community_with_name_members(user, community_name):
    check_is_not_banned_from_community_with_name(user=user, community_name=community_name)

    if Community.is_community_with_name_private(community_name=community_name):
        if not user.is_member_of_community_with_name(community_name=community_name):
            raise ValidationError(
                'Нельзя видеть подписчиков частного сообщества.',
            )


def check_can_join_community_with_name(user, community_name):
    if user.is_banned_from_community_with_name(community_name):
        raise ValidationError('Вы не можете присоединиться к сообществу, в котором вы были заблокированы.')

    if user.is_member_of_community_with_name(community_name):
        raise ValidationError(
            'Вы уже являетесь подписчиков сообщества',
        )

    if Community.is_community_with_name_private(community_name=community_name):
        if not user.is_invited_to_community_with_name(community_name=community_name):
            raise ValidationError(
                'Вы не приглашены в это сообщество',
            )


def check_can_leave_community_with_name(user, community_name):
    if not user.is_member_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Вы не можете покинуть сообщество, подписчиком которого Вы не являетесь.',
        )

    if user.is_creator_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Вы не можете покинуть созданное Вами сообщество.',
        )


def check_can_invite_user_with_username_to_community_with_name(user, username, community_name):
    if not user.is_member_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Вы можете приглашать людей только в сообщество, членом которого являетесь.',
        )

    if user.has_invited_user_with_username_to_community_with_name(username=username, community_name=community_name):
        raise ValidationError(
            'Вы уже пригласили этого пользователя присоединиться к сообществу.',
        )

    if Community.is_user_with_username_member_of_community_with_name(username=username,
                                                                     community_name=community_name):
        raise ValidationError(
            'Пользователь уже является подписчиком сообщества',
        )

    if not Community.is_community_with_name_invites_enabled(community_name=community_name) and not (
            user.is_administrator_of_community_with_name(
                community_name=community_name) or user.is_moderator_of_community_with_name(
        community_name=community_name)):
        raise ValidationError(
            'Приглашения для этого сообщества не включены. Приглашать могут только администраторы и модераторы.',
        )


def check_can_uninvite_user_with_username_to_community_with_name(user, username, community_name):
    if not user.has_invited_user_with_username_to_community_with_name(username=username,
                                                                      community_name=community_name):
        raise ValidationError(
            'Никаких приглашений не найдено',
        )


def check_can_get_community_with_name_banned_users(user, community_name):
    if not user.is_administrator_of_community_with_name(
            community_name=community_name) and not user.is_moderator_of_community_with_name(
        community_name=community_name):
        raise ValidationError(
            'Только администраторы и модераторы сообщества могут видеть заблокированных пользователей.',
        )


def check_can_ban_user_with_username_from_community_with_name(user, username, community_name):
    if not user.is_administrator_of_community_with_name(
            community_name=community_name) and not user.is_moderator_of_community_with_name(
        community_name=community_name):
        raise ValidationError(
            'Только администраторы и модераторы сообщества могут блокировать участников сообщества.',
        )

    if Community.is_user_with_username_banned_from_community_with_name(username=username,
                                                                       community_name=community_name):
        raise ValidationError(
            'Пользователь уже забанен',
        )

    if Community.is_user_with_username_moderator_of_community_with_name(username=username,
                                                                        community_name=community_name) or Community.is_user_with_username_administrator_of_community_with_name(
        username=username, community_name=community_name):
        raise ValidationError(
            'Вы не можете заблокировать модератора или администратора сообщества',
        )


def check_can_unban_user_with_username_from_community_with_name(user, username, community_name):
    if not user.is_administrator_of_community_with_name(
            community_name=community_name) and not user.is_moderator_of_community_with_name(
        community_name=community_name):
        raise ValidationError(
            'Только администраторы и модераторы сообщества могут блокировать участников сообщества',
        )
    if not Community.is_user_with_username_banned_from_community_with_name(username=username,
                                                                           community_name=community_name):
        raise ValidationError(
            'Нельзя разбанить не заблокированного пользователя',
        )


def check_can_add_administrator_with_username_to_community_with_name(user, username, community_name):
    if not user.is_creator_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Только создатель сообщества может добавить администраторов.',
        )

    if Community.is_user_with_username_administrator_of_community_with_name(username=username,
                                                                            community_name=community_name):
        raise ValidationError(
            'Пользователь уже является администратором',
        )

    if not Community.is_user_with_username_member_of_community_with_name(username=username,
                                                                        community_name=community_name):
        raise ValidationError(
            'Нельзя сделать администратором пользователя, который не подписан на сообщество',
        )


def check_can_remove_administrator_with_username_to_community_with_name(user, username, community_name):
    if not user.is_creator_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Только создатель сообщества может удалить администраторов.',
        )

    if not Community.is_user_with_username_administrator_of_community_with_name(username=username,
                                                                                community_name=community_name):
        raise ValidationError(
            'Пользователь не является администратором',
        )


def check_can_get_community_with_name_administrators(user, community_name):
    check_is_not_banned_from_community_with_name(user=user, community_name=community_name)


def check_can_add_moderator_with_username_to_community_with_name(user, username, community_name):
    if not user.is_administrator_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Только администраторы сообщества могут добавлять модераторов',
        )

    if Community.is_user_with_username_administrator_of_community_with_name(username=username,
                                                                            community_name=community_name):
        raise ValidationError(
            'Пользователь является администратором',
        )

    if Community.is_user_with_username_moderator_of_community_with_name(username=username,
                                                                        community_name=community_name):
        raise ValidationError(
            'Пользователь уже является модератором',
        )

    if not Community.is_user_with_username_member_of_community_with_name(username=username,
                                                                         community_name=community_name):
        raise ValidationError(
            'Нельзя сделать модератором пользователя, который не является подписчиком сообщества',
        )


def check_can_remove_moderator_with_username_to_community_with_name(user, username, community_name):
    if not user.is_administrator_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Удалять модераторов могут только администраторы сообщества',
        )

    if not Community.is_user_with_username_moderator_of_community_with_name(username=username,
                                                                            community_name=community_name):
        raise ValidationError(
            'Пользователь не является модератором',
        )


def check_can_get_community_with_name_moderators(user, community_name):
    check_is_not_banned_from_community_with_name(user=user, community_name=community_name)


def check_is_not_banned_from_community_with_name(user, community_name):
    if user.is_banned_from_community_with_name(community_name):
        raise PermissionDenied('Вы заблокированы в этом сообществе')


def check_can_favorite_community_with_name(user, community_name):
    if not user.is_member_of_community_with_name(community_name=community_name):
        raise ValidationError(
            'Вы должны быть членом сообщества, прежде чем сделать его избранным',
        )

    if user.has_favorite_community_with_name(community_name=community_name):
        raise ValidationError(
            'Вы уже отметили это сообщество как избранное',
        )


def check_can_exclude_community(user, community):
    if user.has_excluded_community_with_name(community_name=community.name):
        raise ValidationError(
            'Вы уже отметили это сообщество как исключенное',
        )

    if community.type == Community.COMMUNITY_TYPE_PRIVATE:
        raise ValidationError(
            'Частные сообщества не могут создавать особые записи',
        )


def check_can_remove_exclusion_for_community(user, community):
    if not user.has_excluded_community_with_name(community_name=community.name):
        raise ValidationError(
            'Вы не отметили это сообщество как исключенное',
        )


def check_can_unfavorite_community_with_name(user, community_name):
    if not user.has_favorite_community_with_name(community_name=community_name):
        raise ValidationError(
            'Вы не фаворит общества',
        )


def check_can_get_community_with_name(user, community_name):
    check_is_not_banned_from_community_with_name(user=user, community_name=community_name)


def check_is_staff_of_community_with_name(user, community_name):
    if not user.is_staff_of_community_with_name(community_name=community_name):
        raise PermissionDenied('Не персонал сообщества')
