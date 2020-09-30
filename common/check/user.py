from rest_framework.exceptions import PermissionDenied, ValidationError
from django.conf import settings

def check_can_connect_with_user(user, user_id):
    check_user_not_blocked(user=user, user_id=user_id)
    check_is_not_connected(user=user, user_id=user_id)
    check_has_not_reached_max_connections(user=user)

def check_can_follow_user(user, user_id):
    check_user_not_blocked(user=user, user_id=user_id)
    check_user_not_following(user_id=user_id, user=user)
    check_has_not_reached_max_follows(user=user)

def check_not_can_follow_user(user, user_id):
    check_user_not_blocked(user=user, user_id=user_id)
    check_is_following_user(user=user, user_id=user_id)
    check_has_not_reached_max_follows(user=user)

def check_can_block_user(user, user_id):
    if user_id == user.pk:
        raise ValidationError('Вы не можете блокировать себя')
    check_user_not_blocked(user=user, user_id=user_id)
def check_has_not_reached_max_connections(user):
    if user.count_connections() > settings.USER_MAX_CONNECTIONS:
        raise ValidationError('Достигнуто максимальное количество друзей',)

def check_can_unblock_user(user, user_id):
    if not user.has_blocked_user_with_id(user_id=user_id):
        raise ValidationError('Вы не можете разблокировать учетную запись, которую вы не заблокировали')

def check_is_following_user(user, user_id):
    if not user.is_following_user_with_id(user_id):
        return True

def check_user_not_following(user, user_id):
    if user.is_following_user_with_id(user_id):
        raise ValidationError('Вы уже подписаны на этого пользователя',)


def check_has_not_reached_max_follows(user):
    if user.count_following() > settings.USER_MAX_FOLLOWS:
        raise ValidationError('Достигнуто максимальное количество подписчиков',)

def check_user_not_blocked(user, user_id):
    if user.is_blocked_with_user_with_id(user_id=user_id):
        raise PermissionDenied('Вы в черном списке у этого пользователя.')

def check_user_connected(user, request_user):
    if not request_user.is_connected_with_user_with_id(user.pk):
        raise ValidationError('Не дружит с пользователем.')

def check_is_not_connected(user, user_id):
    if user.is_connected_with_user_with_id(user_id):
        raise ValidationError('Пользователь уже в друзьях',)

def check_user_can_get_list(request_user, user):
    check_user_not_blocked(request_user, user.pk)
    if user.is_closed_profile():
        if request_user.is_followers_user_with_id(user_id=user.pk) or request_user.is_connected_with_user_with_id(user_id=user.pk):
            return True
        else:
            raise PermissionDenied('Ошибка доступа',)
    elif request_user.is_child() and not user.is_child_safety():
        raise PermissionDenied('Это не проверенный профиль, поэтому может навредить ребенку.')
    else:
        return True

def check_anon_user_can_get_list(user):
    if user.is_closed_profile():
        raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
    elif not user.is_child_safety():
        raise PermissionDenied('Это не проверенный профиль, поэтому может навредить ребенку.')
    else:
        return True
