import re
from rest_framework.exceptions import PermissionDenied
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


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

def get_detail_template_community(community, folder, template, request):
    if request.user.is_authenticated and request.user.is_member_of_community_with_name(community.name):
        if request.user.is_moderator_of_community_with_name(community.name):
            template_name = folder + "moderator_" + template
        elif request.user.is_administrator_of_community_with_name(community.name):
            template_name = folder + "admin_" + template
        elif request.user.is_editor_of_community_with_name(community.name):
            template_name = folder + "admin_" + template
        else:
            template_name = folder + template
    elif request.user.is_authenticated and community.is_public():
        template_name = folder + template
    elif request.user.is_anonymous and community.is_public():
        template_name = folder + "anon_" + template
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        template_name = "mob_" + template_name
    return template_name
