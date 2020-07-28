import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from rest_framework.exceptions import PermissionDenied
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


def get_default_template(folder, template, request):
    import re

    if request.user.is_authenticated:
        template_name = folder + template
    elif request.user.is_anonymous:
        template_name = folder + "anon_" + template

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        template_name = "mob_" + template_name
    return template_name
