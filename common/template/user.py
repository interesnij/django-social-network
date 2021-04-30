from common.utils import update_activity, get_folder
from rest_framework.exceptions import PermissionDenied


def get_template_user(user, folder, template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.is_no_phone_verified():
            template_name = "main/phone_verification.html"
        elif user.pk == request_user.pk:
            if user.is_suspended():
                template_name = "generic/u_template/you_suspended.html"
            elif user.is_deleted():
                template_name = "generic/u_template/you_deleted.html"
            elif user.is_blocked():
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
            elif request_user.is_manager() or request_user.is_superuser:
                template_name = folder + "staff_" + template
                request_user.create_or_plus_populate_friend(user.pk)
            elif request_user.is_blocked_with_user_with_id(user_id=user.pk):
                template_name = "generic/u_template/block_user.html"
            elif request_user.is_connected_with_user_with_id(user_id=user.pk):
                template_name = folder + template
                request_user.create_or_plus_populate_friend(user.pk)
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

def get_settings_template(template, request_user, user_agent):
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.is_no_phone_verified():
            template_name = "main/phone_verification.html"
        elif request_user.is_suspended():
            template_name = "generic/u_template/you_suspended.html"
        elif request_user.is_deleted():
            template_name = "generic/u_template/you_deleted.html"
        elif request_user.is_blocked():
            template_name = "generic/u_template/you_global_block.html"
        else:
            template_name = template
    elif request_user.is_anonymous:
        raise PermissionDenied("Ошибка доступа")
    return get_folder(user_agent) + template_name


def get_default_template(folder, template, request_user, user_agent):
    """ получаем шаблон для любого пользователя. """
    if request_user.is_authenticated:
        template_name = folder + template
    elif request_user.is_anonymous:
        template_name = folder + "anon_" + template

    return get_folder(user_agent) + template_name

def get_detect_platform_template(template, request_user, user_agent):
    """ получаем шаблон для зарегистрированного пользователя. Анонимов не пускаем."""
    if request_user.is_anonymous:
        raise PermissionDenied("Ошибка доступа")
    elif request_user.is_no_phone_verified():
        template = "main/phone_verification.html"

    return get_folder(user_agent) + template_name

def render_for_platform(request, template, data):
    from django.shortcuts import render
    return render(request, get_folder(request.META['HTTP_USER_AGENT']) + template, data)

def get_detect_main_template(template, request_user, user_agent):
    """ получаем название шаблона для новостей и рекомендаций. Направляем или в новости, или на страницу входа, исходя из платформы пользователя """
    if request_user.is_authenticated:
        update_activity(request_user, user_agent)
        if request_user.is_no_phone_verified():
            template_name = "main/phone_verification.html"
        elif request_user.is_suspended():
            template_name = "generic/u_template/you_suspended.html"
        elif request_user.is_deleted():
            template_name = "generic/u_template/you_deleted.html"
        elif request_user.is_blocked():
            template_name = "generic/u_template/you_global_block.html"
        else:
            template_name = template
    elif request_user.is_anonymous:
        template_name = "main/auth/auth.html"
    return get_folder(user_agent) + template_name
