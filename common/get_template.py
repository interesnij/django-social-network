import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from rest_framework.exceptions import PermissionDenied
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id, check_can_get_posts_for_community_with_name


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

def get_detail_template_community_photo(community, folder, template, request_user):
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

def get_detail_template_user_photo(user, folder, template, request_user):
    if request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            template_name = "main/phone_verification.html"
        elif user.pk == request_user.pk:
            if user.is_suspended():
                template_name = "generic/template/you_suspended.html"
            elif user.is_blocked():
                template_name = "generic/template/you_global_block.html"
            else:
                template_name = folder + "my_" + template
        elif request_user.is_photo_manager():
            template_name = folder + "staff_" + template
        elif request_user.pk != user.pk:
            if user.is_suspended():
                template_name = "generic/template/user_suspended.html"
            elif user.is_blocked():
                template_name = "generic/template/user_global_block.html"
            elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
                raise PermissionDenied('Ошибка доступа')
            elif user.is_closed_profile():
                if request_user.is_followers_user_with_id(user_id=user.pk) or request_user.is_connected_with_user_with_id(user_id=user.pk):
                    template_name = folder + template
                else:
                    raise PermissionDenied('Ошибка доступа')
            else:
                template_name = folder + template
    elif request_user.is_anonymous:
        if user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        else:
            template_name = folder + "anon_" + template

    return template_name

def get_default_template(folder, template, request):
    import re

    if request.user.is_authenticated:
        template_name = folder + template
    elif request.user.is_anonymous:
        template_name = folder + "anon_" + template

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        template_name = "mob_" + template_name
    return template_name
