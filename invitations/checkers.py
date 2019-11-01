from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, AuthenticationFailed
from invitations.models import UserInvite


def check_can_create_invite(user, nickname):
    if user.invite_count == 0:
        raise ValidationError('У вас не осталось приглашений')

    if UserInvite.objects.filter(invited_by=user, nickname=nickname).exists():
        raise ValidationError('Ник уже используется')


def check_can_update_invite(user, invite_id):
    check_is_creator_of_invite_with_id(user=user, invite_id=invite_id)


def check_can_send_email_invite_to_invite_id(user, invite_id, email):
    check_is_creator_of_invite_with_id(user=user, invite_id=invite_id)
    invite = UserInvite.objects.get(id=invite_id)
    if invite.email == email:
        raise ValidationError('Приглашение по электронной почте уже отправлено на этот адрес')


def check_can_delete_invite_with_id(user, invite_id):
    check_is_creator_of_invite_with_id(user=user, invite_id=invite_id)
    check_if_invite_is_not_used(user=user, invite_id=invite_id)


def check_if_invite_is_not_used(user, invite_id):
    invite = UserInvite.objects.get(id=invite_id)
    if invite.created_user:
        raise ValidationError('Приглашение уже используется и не может быть удалено')


def check_is_creator_of_invite_with_id(user, invite_id):
    if not UserInvite.objects.filter(id=invite_id, invited_by=user).exists():
        raise ValidationError('Приглашение не было создано Вами')
