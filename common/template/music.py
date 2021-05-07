from common.utils import update_activity, get_folder
from rest_framework.exceptions import PermissionDenied


def get_template_community_music(list, folder, template, request_user, user_agent, staff):
    community = list.community
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.type[0] == "_":
            if request_user.is_no_phone_verified():
                template_name = "main/phone_verification.html"
            elif request_user.is_deleted():
                template_name = "generic/u_template/you_deleted.html"
            elif request_user.is_closed():
                template_name = "generic/u_template/you_closed.html"
            elif request_user.is_suspended():
                template_name = "generic/u_template/you_suspended.html"
        elif community.type[0] == "_":
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
        elif playlist.type[0] == "_":
            if playlist.is_deleted():
                if request_user.is_administrator_of_community(community.pk) and playlist.community.pk == community.pk:
                    template_name = folder + "admin_deleted_" + template
                else:
                    template_name = "generic/c_template/list_deleted.html"
            elif playlist.is_closed():
                if staff:
                    template_name = folder + "staff_closed_" + template
                if request_user.is_administrator_of_community(community.pk) and playlist.community.pk == community.pk:
                    template_name = "generic/c_template/admin_list_closed.html"
                else:
                    template_name = "generic/c_template/list_closed.html"
            elif playlist.is_suspended():
                if staff:
                    template_name = folder + "staff_suspended_" + template
                if request_user.is_administrator_of_community(community.pk) and playlist.community.pk == community.pk:
                    template_name = "generic/c_template/admin_list_suspended.html"
                else:
                    template_name = "generic/c_template/list_suspended.html"
        elif request_user.is_member_of_community(community.pk):
            if request_user.is_administrator_of_community(community.pk):
                template_name = folder + "admin_" + template
            elif staff:
                template_name = folder + "staff_member_" + template
            elif playlist.is_private():
                template_name = folder + "private_" + template
            else:
                template_name = folder + "member_" + template
        elif staff:
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
            if playlist.is_private():
                template_name = folder + "private_" + template
            elif request_user.is_child() and not community.is_verified():
                template_name = "generic/c_template/no_child_safety.html"
            else:
                template_name = folder + "public_" + template
    elif request_user.is_anonymous:
        if community.type[0] == "_":
            if community.is_suspended():
                template_name = "generic/c_template/anon_community_suspended.html"
            elif community.is_deleted():
                template_name = "generic/c_template/anon_community_deleted.html"
            elif community.is_closed():
                template_name = "generic/c_template/anon_community_closed.html"
        elif playlist.type[0] == "_":
            if playlist.is_deleted():
                template_name = "generic/c_template/anon_list_deleted.html"
            elif playlist.is_closed():
                template_name = "generic/c_template/anon_list_closed.html"
            elif playlist.is_suspended():
                template_name = "generic/c_template/anon_list_suspended.html"
        elif community.is_public():
            if not community.is_verified():
                template_name = "generic/c_template/anon_no_child_safety.html"
            else:
                template_name = folder + "anon_" + template
        elif community.is_close():
            template_name = "generic/c_template/anon_close_community.html"
        elif community.is_private():
            template_name = "generic/c_template/anon_private_community.html"
    return get_folder(user_agent) + template_name

def get_permission_community_music(playlist, folder, template, request_user, user_agent):
    from common.check.community import check_can_get_lists, check_anon_can_get_list
    community = playlist.community

    if community.type[0] == "_":
        raise PermissionDenied('Ошибка доступа')
    elif request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            template_name = "main/phone_verification.html"
        elif request_user.is_staff_of_community(community.pk):
            template_name = folder + "admin_" + template
        elif request_user.is_audio_manager():
            template_name = folder + "staff_" + template
        elif check_can_get_lists(request_user, community):
            template_name = folder + template
        elif community.is_public():
            template_name = folder + template
        else:
            raise PermissionDenied('Ошибка доступа')
    elif request_user.is_anonymous:
        if check_anon_can_get_list(community):
            template_name = folder + "anon_" + template
        else:
            raise PermissionDenied('Ошибка доступа')
    return get_folder(user_agent) + template_name

def get_template_user_music(playlist, folder, template, request_user, user_agent):
    user = playlist.creator
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.is_no_phone_verified():
            template_name = "main/phone_verification.html"
        elif user.pk == request_user.pk:
            if request_user.is_suspended():
                template_name = "generic/u_template/you_suspended.html"
            elif request_user.is_deleted():
                template_name = "generic/u_template/you_deleted.html"
            elif request_user.is_blocked():
                template_name = "generic/u_template/you_global_block.html"
            else:
                template_name = folder + "my_" + template
        elif request_user.pk != user.pk:
            if user.is_suspended():
                template_name = "generic/u_template/user_suspended.html"
            elif user.is_deleted():
                template_name = "generic/u_template/user_deleted.html"
            elif user.is_blocked():
                template_name = "generic/u_template/user_global_block.html"
            elif request_user.is_audio_manager() or request_user.is_superuser:
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
        elif user.is_deleted():
            template_name = "generic/u_template/anon_user_deleted.html"
        elif user.is_blocked():
            template_name = "generic/u_template/anon_user_global_block.html"
        elif user.is_closed_profile():
            template_name = "generic/u_template/anon_close_user.html"
        elif not user.is_child_safety():
            template_name = "generic/u_template/anon_no_child_safety.html"
        else:
            template_name = folder + "anon_" + template
    return get_folder(user_agent) + template_name

def get_permission_user_music(playlist, folder, template, request_user, user_agent):
    from common.check.user import check_user_can_get_list, check_anon_user_can_get_list
    user = playlist.creator

    if user.type[0] == "_":
        raise PermissionDenied('Ошибка доступа')
    elif request_user.is_authenticated:
        if request_user.is_no_phone_verified():
            raise PermissionDenied('Ошибка доступа')
        elif user.pk == request_user.pk:
            template_name = folder + "my_" + template
        elif request_user.is_audio_manager():
            template_name = folder + "staff_" + template
        elif request_user.pk != user.pk:
            if check_user_can_get_list(request_user, user):
                template_name = folder + template
    elif request_user.is_anonymous:
        if check_anon_user_can_get_list(user):
            template_name = folder + "anon_" + template
    return get_folder(user_agent) + template_name
