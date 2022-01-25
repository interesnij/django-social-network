from rest_framework.exceptions import PermissionDenied
import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)


def update_activity(user, user_agent):
    from datetime import datetime, timedelta

    if MOBILE_AGENT_RE.match(user_agent):
        user.last_activity, user.device = datetime.now(), "Ph"
        user.save(update_fields=['last_activity', 'device'])
    else:
        user.last_activity, user.device = datetime.now(), "De"
        user.save(update_fields=['last_activity', 'device'])


def get_folder(user_agent):
    if MOBILE_AGENT_RE.match(user_agent):
        return "mobile/"
    else:
        return "desctop/"

def get_fine_request_user(request_user):
    if request_user.is_deleted():
        template = "generic/u_template/you_deleted.html"
    elif request_user.is_closed():
        template = "generic/u_template/you_closed.html"
    elif request_user.is_suspended():
        template = "generic/u_template/you_suspended.html"
    return template

def get_fine_community_item(request_user, community, item, folder, template):
    if item.is_deleted():
        if request_user.is_administrator_of_community(community.pk) and item.community.pk == community.pk:
            template = folder + "admin_deleted_" + template
        else:
            template =  "generic/c_template/deleted.html"
    elif item.is_closed():
        if staff:
            template = folder + "staff_closed_" + template
        if request_user.is_administrator_of_community(community.pk) and item.community.pk == community.pk:
            template = "generic/c_template/admin_closed.html"
        else:
            template =  folder + "closed_" + template
    elif item.is_suspended():
        if staff:
            template = folder + "staff_suspended_" + template
        if request_user.is_administrator_of_community(community.pk) and item.community.pk == community.pk:
            template = "generic/c_template/admin_suspended.html"
        else:
            template = "generic/c_template/suspended.html"
    return template
def get_anon_fine_community_item(community, item):
    if item.is_deleted():
        template = "generic/c_template/anon_deleted.html"
    elif item.is_closed():
        template = "generic/c_template/anon_closed.html"
    elif item.is_suspended():
        template = "generic/c_template/anon_suspended.html"
    return template
def get_anon_fine_user_item(item):
    if item.is_deleted():
        template = "generic/u_template/anon_deleted.html"
    elif item.is_closed():
        template = folder + "anon_closed_" + template
    elif item.is_suspended():
        template = "generic/u_template/anon_suspended.html"
    return template
def get_fine_user_item(request_user, item, folder, template):
    if item.is_deleted():
        if item.creator.pk == request_user.pk:
            template = folder + "my_deleted_" + template
        else:
            template = "generic/u_template/deleted.html"
    elif item.is_closed():
        if item.creator.pk == request_user.pk:
            template = folder + "my_closed_" + template
        else:
            template = folder + "closed_" + template
    elif item.is_suspended():
        if item.creator.pk == request_user.pk:
            template = folder + "my_suspended_" + template
        else:
            template = "generic/u_template/suspended.html"
    return template
def get_fine_user(user):
    if user.is_suspended():
        template = "generic/u_template/user_suspended.html"
    elif user.is_deleted():
        template = "generic/u_template/deleted_user.html"
    elif user.is_closed():
        template = "generic/u_template/closed_user.html"
    return template
def get_anon_fine_user(user):
    if user.is_suspended():
        template = "generic/u_template/anon_user_suspended.html"
    elif user.is_deleted():
        template = "generic/u_template/anon_deleted_user.html"
    elif user.is_closed():
        template = "generic/u_template/anon_closed_user.html"
    return template
def get_fine_community(community, request_user):
    if community.is_suspended():
        if request_user.is_administrator_of_community(community.pk):
            template_name = "generic/c_template/admin_community_suspended.html"
        else:
            template_name = "generic/c_template/community_suspended.html"
    elif community.is_deleted():
        if request_user.is_administrator_of_community(community.pk):
            template_name = "generic/c_template/admin_community_deleted.html"
        else:
            template_name = "generic/c_template/community_deleted.html"
    elif community.is_closed():
        if request_user.is_administrator_of_community(community.pk):
            template_name = "generic/c_template/admin_community_closed.html"
        else:
            template_name = "generic/c_template/community_closed.html"
    return template_name
def get_anon_fine_community(community):
    if community.is_suspended():
        template_name = "generic/c_template/anon_community_suspended.html"
    elif community.is_deleted():
        template_name = "generic/c_template/anon_community_deleted.html"
    elif community.is_closed():
        template_name = "generic/c_template/anon_community_closed.html"
    return template_name

def get_fine_anon_user(user):
    if user.is_suspended():
        template = "generic/u_template/anon_user_suspended.html"
    elif user.is_deleted():
        template = "generic/u_template/anon_user_deleted.html"
    elif user.is_closed():
        template = "generic/u_template/anon_user_closed.html"
    return template
def get_anon_fine_user_list(list):
    if list.is_deleted():
        template = "generic/u_template/anon_deleted.html"
    elif list.is_closed():
        template = "generic/u_template/anon_closed.html"
    elif list.is_suspended():
        template = "generic/u_template/anon_suspended.html"
    return template

def get_my_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        else:
            template_name = template
    elif request_user.is_anonymous:
        raise PermissionDenied("Ошибка доступа")
    return get_folder(user_agent) + template_name

def get_admin_template(community, template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        elif community.type[0] == "_":
            template_name = get_fine_community(community, request_user)
        else:
            template_name = template
    elif request_user.is_anonymous:
        raise PermissionDenied("Ошибка доступа")
    return get_folder(user_agent) + template_name

def get_template_community(community, folder, template, request_user, user_agent):
    update_activity(request_user, user_agent)
    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif community.type[0] == "_":
        template_name = get_fine_community(community, request_user)
    elif request_user.is_member_of_community(community.pk):
        if request_user.is_administrator_of_community(community.pk):
            template_name = folder + "admin_" + template
        elif request_user.is_community_manager():
            template_name = folder + "staff_member_" + template
        else:
            template_name = folder + template
    elif request_user.is_community_manager():
        template_name = folder + "staff_" + template
    elif community.is_close():
        if request_user.is_follow_from_community(community.pk):
            template_name = "generic/c_template/follow_community.html"
        else:
            template_name = "generic/c_template/close_community.html"
    elif community.is_private():
        template_name = "generic/c_template/private_community.html"
    elif request_user.is_banned_from_community(community.pk):
        template_name = "generic/c_template/block_community.html"
    elif community.is_public():
        if request_user.is_child() and not community.is_verified():
            template_name = "generic/c_template/no_child_safety.html"
        else:
            template_name = folder + "public_" + template
    return get_folder(user_agent) + template_name

def get_template_anon_community(community, template, request_user, user_agent):
    if community.type[0] == "_":
        template_name = get_anon_fine_community(community)
    elif community.is_public():
        if not community.is_verified():
            template_name = "generic/c_template/anon_no_child_safety.html"
        else:
            template_name = template
    elif community.is_close():
        template_name = "generic/c_template/anon_close_community.html"
    elif community.is_private():
        template_name = "generic/c_template/anon_private_community.html"
    return get_folder(user_agent) + template_name

def get_template_user(user, folder, template, request_user, user_agent):
    update_activity(request_user, user_agent)
    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif user.pk == request_user.pk:
            template_name = folder + "my_" + template
    elif request_user.pk != user.pk:
        if user.type[0] == "_":
            template_name = get_fine_user(user)
        elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
            template_name = "generic/u_template/block_user.html"
        elif user.is_closed_profile():
            if request_user.is_followers_user_with_id(user_id=user.pk) or request_user.is_connected_with_user_with_id(user_id=user.pk):
                template_name = folder + template
            else:
                template_name = "generic/u_template/close_user.html"
        elif request_user.is_child() and not user.is_child_safety():
            template_name = "generic/u_template/no_child_safety.html"
        else:
            template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_user(user, template, user_agent):
    if user.type[0] == "_":
        template_name = get_anon_fine_user(user)
    elif user.is_closed_profile():
        template_name = "generic/u_template/anon_close_user.html"
    elif not user.is_child_safety():
        template_name = "generic/u_template/anon_no_child_safety.html"
    else:
        template_name = template
    return get_folder(user_agent) + template_name

def get_template_comments(item, template, request_user, user_agent):
    user = item.creator
    if request_user.is_authenticated:
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        elif user.type[0] == "_":
            template_name = get_fine_user(user)
        elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
            template_name = "generic/u_template/block_user.html"
        elif item.list.is_user_can_see_comment(request_user.pk):
            template_name = folder + template
    else:
        if user.type[0] == "_":
            template_name = get_anon_fine_user(user)
        elif item.list.is_anon_user_can_see_comment():
            template_name = folder + "anon_" + template
    return get_folder(user_agent) + template_name

def get_template_user_item(item, folder, template, request_user, user_agent):
    user, list = item.creator, item.list
    update_activity(request_user, user_agent)
    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif item.type[0] == "_" or list.type[0] == "_":
        template_name = get_fine_user_item(request_user, item, folder, template)
    elif user.type[0] == "_":
        template_name = get_fine_user(user)
    elif user.pk == request_user.pk:
        template_name = folder + "my_" + template
    elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
        template_name = "generic/u_template/block_user.html"
    elif user.is_closed_profile() and not (request_user.is_followers_user_with_id(user_id=user.pk) or request_user.is_connected_with_user_with_id(user_id=user.pk)):
        template_name = "generic/u_template/close_user.html"
    elif request_user.is_child() and not user.is_child_safety():
        template_name = "generic/u_template/no_child_safety.html"
    else:
        template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_user_item(item, template, request_user, user_agent):
    user, list = item.creator, item.list
    if user.type[0] == "_":
        template_name = get_anon_fine_user(user)
    elif item.type[0] == "_" or list.type[0] == "_":
        template_name = get_anon_fine_user_list(item)
    elif user.is_closed_profile():
        template_name = "generic/u_template/anon_close_user.html"
    elif not user.is_child_safety():
        template_name = "generic/u_template/anon_no_child_safety.html"
    else:
        template_name = template
    return get_folder(user_agent) + template_name


def get_template_user_list(list, folder, template, request_user, user_agent):
    user = list.creator
    update_activity(request_user, user_agent)
    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif list.type[0] == "_":
        template_name = get_fine_user_item(request_user, list, folder, template)
    elif user.type[0] == "_":
        template_name = get_fine_user(user)
    elif user.pk == request_user.pk:
        template_name = folder + "my_" + template
    elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
        template_name = "generic/u_template/block_user.html"
    elif user.is_closed_profile() and not (request_user.is_followers_user_with_id(user_id=user.pk) or request_user.is_connected_with_user_with_id(user_id=user.pk)):
        template_name = "generic/u_template/close_user.html"
    elif request_user.is_child() and not user.is_child_safety():
        template_name = "generic/u_template/no_child_safety.html"
    else:
        template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_user_list(list, template, request_user, user_agent):
    user = list.creator
    if user.type[0] == "_":
        template_name = get_anon_fine_user(user)
    elif list.type[0] == "_":
        template_name = get_anon_fine_user_list(item)
    elif user.is_closed_profile():
        template_name = "generic/u_template/anon_close_user.html"
    elif not user.is_child_safety():
        template_name = "generic/u_template/anon_no_child_safety.html"
    else:
        template_name = template
    return get_folder(user_agent) + template_name


def get_template_community_item(item, folder, template, request_user, user_agent):
    community, list = item.community, item.list
    update_activity(request_user, user_agent)
    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif community.type[0] == "_":
        template_name = get_fine_community(community, request_user)
    elif item.type[0] == "_" or list.type[0] == "_":
        template_name = get_fine_community_item(request_user, community, item, folder, template)
    elif request_user.is_administrator_of_community(community.pk):
        template_name = folder + "admin_" + template
    elif community.is_private():
        template_name = "generic/c_template/private_community.html"
    elif request_user.is_banned_from_community(community.pk):
        template_name = "generic/c_template/block_community.html"
    elif request_user.is_child() and not community.is_verified():
        template_name = "generic/c_template/no_child_safety.html"
    elif community.is_close() and not request_user.is_member_of_community(community.pk):
         template_name = "generic/c_template/close_community.html"
    else:
        template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_community_item(item, template, request_user, user_agent):
    community, list = item.community, item.list
    if community.type[0] == "_":
        template_name = get_anon_fine_community(community)
    elif item.type[0] == "_" or list.type[0] == "_":
        template_name = get_anon_fine_community_item(community, item)
    elif community.is_public():
        if not community.is_verified():
            template_name = "generic/c_template/anon_no_child_safety.html"
        else:
            template_name = template
    elif community.is_close():
        template_name = "generic/c_template/anon_close_community.html"
    elif community.is_private():
        template_name = "generic/c_template/anon_private_community.html"
    return get_folder(user_agent) + template_name


def get_template_community_list(list, folder, template, request_user, user_agent):
    community = list.community
    update_activity(request_user, user_agent)
    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif community.type[0] == "_":
        template_name = get_fine_community(community, request_user)
    elif list.type[0] == "_":
        template_name = get_fine_community_item(request_user, community, list, folder, template)
    elif request_user.is_administrator_of_community(community.pk):
        template_name = folder + "admin_" + template
    elif community.is_private() and not request_user.is_member_of_community(community.pk):
        template_name = "generic/c_template/private_community.html"
    elif request_user.is_banned_from_community(community.pk):
        template_name = "generic/c_template/block_community.html"
    elif request_user.is_child() and not community.is_verified():
        template_name = "generic/c_template/no_child_safety.html"
    elif community.is_close() and not request_user.is_member_of_community(community.pk):
         template_name = "generic/c_template/close_community.html"
    else:
        template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_anon_community_list(list, template, request_user, user_agent):
    community = list.community
    if community.type[0] == "_":
        template_name = get_anon_fine_community(community)
    elif list.type[0] == "_":
        template_name = get_anon_fine_community_item(community, item)
    elif community.is_public():
        if not community.is_verified():
            template_name = "generic/c_template/anon_no_child_safety.html"
        else:
            template_name = template
    elif community.is_close():
        template_name = "generic/c_template/anon_close_community.html"
    elif community.is_private():
        template_name = "generic/c_template/anon_private_community.html"
    return get_folder(user_agent) + template_name

def get_staff_template(template, request_user, user_agent):
    update_activity(request_user, user_agent)

    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    elif request_user.is_moderator():
        template_name = template
    else:
        raise PermissionDenied("Ошибка доступа")
    return get_folder(user_agent) + template_name

def get_detect_platform_template(template, request_user, user_agent):
    update_activity(request_user, user_agent)

    if request_user.type[0] == "_":
        template_name = get_fine_request_user(request_user)
    else:
        template_name = template
    return get_folder(user_agent) + template_name


def get_default_template(folder, template, request_user, user_agent):
    if request_user.is_authenticated:
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        else:
            template_name = folder + template
        update_activity(request_user, user_agent)
    else:
        template_name = folder + "anon_" + template
    return get_folder(user_agent) + template_name


def get_settings_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        else:
            template_name = template
    elif request_user.is_anonymous:
        raise PermissionDenied("Ошибка доступа")
    return get_folder(user_agent) + template_name

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

def get_detect_platform_template(template, request_user, user_agent):
    """ получаем шаблон для зарегистрированного пользователя. Анонимов не пускаем."""
    if request_user.is_anonymous:
        raise PermissionDenied("Ошибка доступа")
    else:
        template = template
    return get_folder(user_agent) + template

def get_detect_main_template(template, request_user, user_agent):
    """ получаем название шаблона для новостей и рекомендаций. Направляем или в новости, или на страницу входа, исходя из платформы пользователя """
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            template_name = get_fine_request_user(request_user)
        else:
            template_name = template
    elif request_user.is_anonymous:
        template_name = "main/auth/auth.html"
    return get_folder(user_agent) + template_name

def render_for_platform(request, template, data):
    from django.shortcuts import render
    return render(request, get_folder(request.META['HTTP_USER_AGENT']) + template, data)


def get_template_user_chat(chat, folder, template, request_user, user_agent):
    if not request_user.is_authenticated or not chat.is_group() or request_user.type[0] == "_":
        raise PermissionDenied("Ошибка доступа")
    elif chat.creator.pk == request_user.pk:
        template_name = folder + "creator_" + template
    elif request_user.is_administrator_of_chat(chat.pk):
        template_name = folder + "admin_" + template
    elif request_user.is_member_of_chat(chat.pk):
        template_name = folder + template
    return get_folder(user_agent) + template_name

def get_template_admin_chat(chat, template, request_user, user_agent):
    if request_user.is_authenticated and request_user.is_administrator_of_chat(chat.pk) and not request_user.type[0] == "_":
        return get_folder(user_agent) + template
    return False
