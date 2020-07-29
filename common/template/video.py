from rest_framework.exceptions import PermissionDenied
from common.check.user import check_user_can_get_list, check_anon_user_can_get_list
from common.check.community import check_can_get_lists, check_anon_can_get_list


def get_template_community_video(community, folder, template, request_user):
    if request_user.is_authenticated:
        if community.is_suspended():
            template_name = "generic/c_template/community_suspended.html"
        elif community.is_blocked():
            template_name = "generic/c_template/community_blocked.html"
        if request_user.is_member_of_community_with_name(community.name):
            if request_user.is_administrator_of_community_with_name(community.name):
                template_name = folder + "admin_" + template
            elif request_user.is_moderator_of_community_with_name(community.name):
                template_name = folder + "moderator_" + template
            elif request_user.is_editor_of_community_with_name(community.name):
                template_name = folder + "editor_" + template
            elif request_user.is_advertiser_of_community_with_name(community.name):
                template_name = folder + "advertiser_" + template
            elif request_user.is_video_manager():
                template_name = folder + "staff_member_" + template
            else:
                template_name = folder + "member_" + template
        elif request_user.is_follow_from_community_with_name(community.pk):
            template_name = "generic/c_template/follow_community.html"
        elif request_user.is_video_manager():
            template_name = folder + "staff_" + template
        elif request_user.is_banned_from_community_with_name(community.name):
            template_name = "generic/c_template/block_community.html"
        elif community.is_public():
            if request_user.is_child() and not community.is_child_safety():
                template_name = "generic/c_template/no_child_safety.html"
            else:
                template_name = folder + "public_" + template
        elif community.is_closed():
            template_name = "generic/c_template/close_community.html"
        elif community.is_private():
            template_name = "generic/c_template/private_community.html"
    elif request_user.is_anonymous:
        if community.is_suspended():
            template_name = "generic/c_template/anon_community_suspended.html"
        elif community.is_blocked():
            template_name = "generic/c_template/anon_community_blocked.html"
        elif community.is_public():
            if not community.is_child_safety():
                template_name = "generic/c_template/anon_no_child_safety.html"
            else:
                template_name = folder + "anon_public_" + template
        elif community.is_closed():
            template_name = "generic/c_template/anon_close_community.html"
        elif community.is_private():
            template_name = "generic/c_template/anon_private_community.html"
    return template_name

def get_permission_community_video(community, folder, template, request_user):
    if community.is_suspended():
        raise PermissionDenied('Ошибка доступа')
    elif community.is_blocked():
        raise PermissionDenied('Ошибка доступа')
    elif request_user.is_authenticated:
        if request_user.is_staff_of_community_with_name(community.name):
            template_name = folder + "admin_" + template
        elif request_user.is_video_manager():
            template_name = folder + "staff_" + template
        elif check_can_get_lists(request_user, community):
            template_name = folder + template
        elif community.is_public():
            template_name = folder + template
        else:
            raise PermissionDenied('Ошибка доступа')
    elif request_user.is_anonymous:
        if check_can_get_lists(community):
            template_name = folder + "anon_" + template
        else:
            raise PermissionDenied('Ошибка доступа')
    return template_name

def get_template_user_video(user, folder, template, request_user):
    if request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            template_name = "main/phone_verification.html"
        elif user.pk == request_user.pk:
            if user.is_suspended():
                template_name = "generic/u_template/you_suspended.html"
            elif user.is_blocked():
                template_name = "generic/u_template/you_global_block.html"
            else:
                template_name = folder + "my_" + template
        elif request_user.pk != user.pk:
            if user.is_suspended():
                template_name = "generic/u_template/user_suspended.html"
            elif user.is_blocked():
                template_name = "generic/u_template/user_global_block.html"
            elif request_user.is_video_manager() or request_user.is_superuser:
                template_name = folder + "staff_" + template
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
    elif request_user.is_anonymous:
        if user.is_suspended():
            template_name = "generic/u_template/anon_user_suspended.html"
        elif user.is_blocked():
            template_name = "generic/u_template/anon_user_global_block.html"
        elif user.is_closed_profile():
            template_name = "generic/u_template/anon_close_user.html"
        elif not user.is_child_safety():
            template_name = "generic/u_template/anon_no_child_safety.html"
        else:
            template_name = folder + "anon_" + template
    return template_name

def get_permission_user_video(user, folder, template, request_user):
    if user.is_suspended():
        raise PermissionDenied('Ошибка доступа')
    elif user.is_blocked():
        raise PermissionDenied('Ошибка доступа')
    elif request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            raise PermissionDenied('Ошибка доступа')
        elif user.pk == request_user.pk:
            template_name = folder + "my_" + template
        elif request_user.is_video_manager():
            template_name = folder + "staff_" + template
        elif request_user.pk != user.pk:
            if check_user_can_get_list(request_user, user):
                template_name = folder + template
    elif request_user.is_anonymous:
        if check_anon_user_can_get_list(user):
            template_name = folder + "anon_" + template
    return template_name
