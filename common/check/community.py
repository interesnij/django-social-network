from rest_framework.exceptions import PermissionDenied


def check_user_not_banned(user, community_pk):
    if user.banned_of_communities.filter(pk=community_pk).values("pk").exists():
        raise PermissionDenied('Вы заблокированы в этом сообществе')

def check_can_get_lists(user, community):
    check_user_not_banned(user=user, community_pk=community.pk)
    if community.is_private() and not user.is_member_of_community_with_name(community_name=community.name):
        raise ValidationError(
            'Сообщество является приватным. Вы должны стать участником, чтобы видеть его записи.',
        )
    elif community.is_closed() and not user.is_member_of_community_with_name(community_name=community.name):
        raise ValidationError(
            'Сообщество является закрытым. Вы должны стать участником, чтобы видеть его записи.',
        )
    elif not community.is_verified() and user.is_child():
        raise ValidationError(
            'Сообщество не проверено. Вы должны стать участником, чтобы видеть его записи.',
        )
    else:
        return True

def check_anon_can_get_list(community):
    if community.is_public() and community.is_verified():
        return True
    else:
        raise ValidationError('Ошибка доступа',)
