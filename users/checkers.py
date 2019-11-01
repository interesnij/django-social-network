from django.conf import settings
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, AuthenticationFailed
import jwt



def check_can_get_user_with_id(user, user_id):
    check_is_not_blocked_with_user_with_id(user=user, user_id=user_id)


def check_password_matches(user, password):
    if not user.check_password(password):
        raise AuthenticationFailed(
            'Неправильный пароль',
        )


def check_can_accept_guidelines(user):
    if user.are_guidelines_accepted:
        raise ValidationError('Вы уже приняли правила пользования сайтом трезвый.рус')


def check_can_block_user_with_id(user, user_id):
    if user_id == user.pk:
        raise ValidationError('Вы не можете блокировать себя')
    check_is_not_blocked_with_user_with_id(user=user, user_id=user_id)


def check_can_unblock_user_with_id(user, user_id):
    if not user.has_blocked_user_with_id(user_id=user_id):
        raise ValidationError('Вы не можете разблокировать учетную запись, которую вы не заблокировали')


def check_is_not_blocked_with_user_with_id(user, user_id):
    if user.is_blocked_with_user_with_id(user_id=user_id):
        raise PermissionDenied('Эта учетная запись заблокирована')


def check_password_reset_verification_token_is_valid(user, password_verification_token):
    try:
        token_contents = jwt.decode(password_verification_token, settings.SECRET_KEY,
                                    algorithm=settings.JWT_ALGORITHM)

        token_user_id = token_contents['user_id']
        token_type = token_contents['type']

        if token_type != user.JWT_TOKEN_TYPE_PASSWORD_RESET:
            raise ValidationError(
                'Тип токена не соответствует'
            )

        if token_user_id != user.pk:
            raise ValidationError(
                'Идентификатор токена пользователя не совпадает'
            )
        return token_user_id
    except jwt.InvalidSignatureError:
        raise ValidationError(
            'Недопустимая подпись токена'
        )
    except jwt.ExpiredSignatureError:
        raise ValidationError(
            'Срок действия токена истек'
        )
    except jwt.DecodeError:
        raise ValidationError(
            'Не удалось декодировать маркер'
        )
    except KeyError:
        raise ValidationError(
            'Недопустимый токен'
        )


def check_email_verification_token_is_valid_for_email(user, email_verification_token):
    try:
        token_contents = jwt.decode(email_verification_token, settings.SECRET_KEY,
                                    algorithm=settings.JWT_ALGORITHM)
        token_email = token_contents['email']
        new_email = token_contents['new_email']
        token_user_id = token_contents['user_id']
        token_type = token_contents['type']

        if token_type != user.JWT_TOKEN_TYPE_CHANGE_EMAIL:
            raise ValidationError(
                'Тип токена не соответствует'
            )

        if token_email != user.email:
            raise ValidationError(
                'Токен электронной почты не соответствует'
            )

        if token_user_id != user.pk:
            raise ValidationError(
                'Идентификатор пользователя маркера не совпадает'
            )
        return new_email
    except jwt.InvalidSignatureError:
        raise ValidationError(
            'Недопустимая подпись токена'
        )
    except jwt.ExpiredSignatureError:
        raise ValidationError(
            'Срок действия токена истек'
        )
    except jwt.DecodeError:
        raise ValidationError(
            'Не удалось декодировать токен'
        )
    except KeyError:
        raise ValidationError(
            'Недопустимый токен'
        )


def check_email_not_taken(user, email):
    if email == user.email:
        return

    if User.is_email_taken(email=email):
        raise ValidationError(
            'Этот email уже получен.'
        )
