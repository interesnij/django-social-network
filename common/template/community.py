from rest_framework.exceptions import PermissionDenied
from common.utils import update_activity, get_folder


def get_community_manage_template(template, request_user, community, user_agent):
    if community.type[0] == "_":
        raise PermissionDenied('Ошибка доступа')
    elif request_user.is_authenticated and request_user.is_administrator_of_community(community.pk):
        template_name = template
        update_activity(request_user, user_agent)
    else:
        raise PermissionDenied('Ошибка доступа.')
    return get_folder(user_agent) + template_name


def get_community_moders_template(template, request_user, community, user_agent):
    if community.type[0] == "_":
        raise PermissionDenied('Ошибка доступа')
    elif request_user.is_authenticated and request_user.is_staff_of_community(community.pk):
        template_name = template
        update_activity(request_user, user_agent)
    else:
        raise PermissionDenied('Ошибка доступа.')
    return get_folder(user_agent) + template_name
