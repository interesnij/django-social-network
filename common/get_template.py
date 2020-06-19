import re
from rest_framework.exceptions import PermissionDenied
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


def get_permission_list_user(user, folder, template, request):

    if user.pk == request.user.pk:
        template_name = folder + "my_" + template
    elif user != request.user and request.user.is_authenticated:
        check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
        template_name = folder + template
        if user.is_closed_profile():
            check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            template_name = folder + template
    elif request.user.is_anonymous and not user.is_closed_profile():
        template_name = folder + template
    elif request.user.is_anonymous and user.is_closed_profile():
        raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        template_name = "mob_" + template_name
    return template_name
