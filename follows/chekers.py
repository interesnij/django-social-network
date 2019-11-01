from django.conf import settings
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, AuthenticationFailed


def check_can_follow_user_with_id(user, user_id):
    check_is_not_blocked_with_user_with_id(user=user, user_id=user_id)
    check_is_not_following_user_with_id(user=user, user_id=user_id)
    check_has_not_reached_max_follows(user=user)


def check_is_not_following_user_with_id(user, user_id):
    if user.is_following_user_with_id(user_id):
        raise ValidationError(
            'Пользователь уже подписан',
        )


def check_has_not_reached_max_follows(user):
    if user.count_following() > settings.USER_MAX_FOLLOWS:
        raise ValidationError(
            'Достигнуто максимальное количество подписчиков',
        )


def check_is_following_user_with_id(user, user_id):
    if not user.is_following_user_with_id(user_id):
        raise ValidationError(
            'Пользователь не подписан',
        )
