import re
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, NotFound

from users.models import User


def username_characters_validator(username):
    if not re.match('^[a-zA-Z0-9_.]*$', username):
        raise ValidationError(
            _('Имена пользователей могут содержать только буквенно-цифровые символы, точки и подчеркивания.'),
        )


def username_not_taken_validator(username):
    if User.is_username_taken(username):
        raise ValidationError(
            _('Имя пользователя уже занято.'),
        )


def email_not_taken_validator(email):
    if User.is_email_taken(email):
        raise ValidationError(
            _('Учетная запись для электронной почты уже существует.'),
        )


def user_username_exists(username):
    if not User.user_with_username_exists(username=username):
        raise NotFound(
            _('Пользователь с указанным именем пользователя не существует.'),
        )


def user_email_exists(email):
    if not User.objects.filter(email=email).exists():
        raise NotFound(
            _('Пользователь с предоставленной электронной почтой не существует.'),
        )
