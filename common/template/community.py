import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from rest_framework.exceptions import PermissionDenied


def get_community_manage_template(template, request_user, community_pk, user_agent):
    if request_user.is_authenticated and request_user.is_administrator_of_community(community_pk):
        template_name = template
    else:
        raise PermissionDenied('Ошибка доступа.')
    if MOBILE_AGENT_RE.match(user_agent):
        template_name = "mobile/" + template_name
    else:
        template_name = "mobile/" + template_name
    return template_name


def get_community_moders_template(template, request_user, community_pk, user_agent):
    if request_user.is_authenticated and request_user.is_administrator_of_community(community_pk) or request_user.is_moderator_of_community(community_pk):
        template_name = template
    else:
        raise PermissionDenied('Ошибка доступа.')
    if MOBILE_AGENT_RE.match(user_agent):
        template_name = "mobile/" + template_name
    else:
        template_name = "mobile/" + template_name
    return template_name
