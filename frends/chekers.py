from django.conf import settings
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, AuthenticationFailed


def check_has_not_reached_max_connections(user):
    if user.count_connections() > settings.USER_MAX_CONNECTIONS:
        raise ValidationError(
            'Достигнуто максимальное количество друзей',
        )


def check_can_connect_with_user_with_id(user, user_id):
    check_is_not_blocked_with_user_with_id(user=user, user_id=user_id)
    check_is_not_connected_with_user_with_id(user=user, user_id=user_id)
    check_has_not_reached_max_connections(user=user)


def check_is_not_connected_with_user_with_id(user, user_id):
    if user.is_connected_with_user_with_id(user_id):
        raise ValidationError(
            'Пользователь уже в друзьях',
        )


def check_is_connected_with_user_with_id(user, user_id):
    if not user.is_connected_with_user_with_id(user_id):
        raise ValidationError(
            'Не дружит с пользователем.',
        )
