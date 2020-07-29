from rest_framework.exceptions import PermissionDenied, ValidationError


def check_user_not_blocked(user, user_id):
    if user.is_blocked_with_user_with_id(user_id=user_id):
        raise PermissionDenied('Вы в черном списке у этого пользователя.')

def check_user_connected(user, user_id):
    if not user.is_connected_with_user_with_id(user_id):
        raise ValidationError('Не дружит с пользователем.')

def check_user_followed(user, user_id):
    if not user.is_followers_user_with_id(user_id=user.pk):
        raise ValidationError('Не дружит с пользователем.')

def check_user_can_get_list(request_user, user):
    check_user_not_blocked(request_user, user.pk)
    if user.is_closed_profile():
        if check_user_connected(request_user, user.pk):
            return True
        elif check_user_followed(request_user, user.pk):
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
