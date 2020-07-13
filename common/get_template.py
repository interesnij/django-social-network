import re
from rest_framework.exceptions import PermissionDenied
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id, check_can_get_posts_for_community_with_name


def get_detail_template_user(user, folder, template, request):
    if user.pk == request.user.pk and request.user.is_authenticated:
        template_name = folder + "my_" + template
    elif user != request.user and request.user.is_authenticated:
        check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
        template_name = folder + template
        if user.is_closed_profile():
            check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            template_name = folder + template
    elif request.user.is_anonymous and not user.is_closed_profile():
        template_name = folder + "anon_" + template
    elif request.user.is_anonymous and user.is_closed_profile():
        raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        template_name = "mob_" + template_name
    return template_name

def get_detail_template_community(community, folder, template, request_user):
    if community.is_suspended():
        raise PermissionDenied('Ошибка доступа')
    elif community.is_blocked():
        raise PermissionDenied('Ошибка доступа')
    elif request_user.is_authenticated:
        if request_user.is_staff_of_community_with_name(community.name):
            template_name = folder + "admin_" + template
        elif request_user.is_community_manager():
            template_name = folder + "staff_" + template
        elif check_can_get_posts_for_community_with_name(request_user, community.name):
            template_name = folder + template
        elif community.is_public():
            template_name = folder + template
        else:
            raise PermissionDenied('Ошибка доступа')
    elif request_user.is_anonymous:
        if community.is_public():
            template_name = folder + "anon_" + template
        elif community.is_closed():
            raise PermissionDenied('Ошибка доступа')
        elif community.is_private():
            raise PermissionDenied('Ошибка доступа')
    return template_name


def get_default_template(folder, template, request):
    import re

    if request.user.is_authenticated:
        template_name = folder + template
    elif request.user.is_anonymous:
        template_name = folder + "anon_" + template

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        template_name = "mob_" + template_name
    return template_name
