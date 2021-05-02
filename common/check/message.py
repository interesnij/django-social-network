from rest_framework.exceptions import PermissionDenied, ValidationError

def check_user_is_admin(user, chat_pk):
    if not user.is_administrator_of_chat(chat_pk):
        raise PermissionDenied('У Вас нет прав администратора')

def check_user_is_member(user, chat_pk):
    if not user.is_member_of_chat(chat_pk):
        raise PermissionDenied('Вы не состоите в чате')

def check_can_send_message(user, chat):
    if user.is_authenticated and not user.type[0] != "_":
        if chat.is_private() and not user.is_member_of_chat(chat.pk):
            raise ValidationError(
                'Чат является приватным.',
            )
    elif user.is_anonymous:
        raise ValidationError('Ошибка доступа.')
    else:
        return True

def check_can_change_chat(user, chat):
    if user.is_authenticated and not user.type[0] != "_":
        if not user.is_administrator_of_chat(chat.pk):
            raise ValidationError(
                'У Вас нет прав доступа.',
            )
    elif user.is_anonymous:
        raise ValidationError('Ошибка доступа.')
    else:
        return True
