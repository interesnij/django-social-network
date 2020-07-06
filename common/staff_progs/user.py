from managers.models import UserStaff, CanWorkStaffUser
from logs.model.manage_user_community import UserWorkerManageLog, UserCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state


def add_user_administrator(user, request_user):
    try:
        user.user_staff.level = "A"
        user.user_staff.save(update_fields=['level'])
    except:
        user_staff = UserStaff.objects.create(user=user, level="A")
    user.is_manager = True
    UserWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_user_moderator(user, request_user):
    try:
        user.user_staff.level = "M"
        user.user_staff.save(update_fields=['level'])
    except:
        user_staff = UserStaff.objects.create(user=user, level="M")
    user.is_manager = True
    UserWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_user_editor(user, request_user):
    try:
        user.user_staff.level = "E"
        user.user_staff.save(update_fields=['level'])
    except:
        user_staff = UserStaff.objects.create(user=user, level="E")
    user.is_manager = True
    UserWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def add_user_advertiser(user, request_user):
    try:
        user.user_staff.level = "R"
        user.user_staff.save(update_fields=['level'])
    except:
        user_staff = UserStaff.objects.create(user=user, level="R")
    user.is_manager = True
    UserWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_user_administrator(user, request_user):
    try:
        user.user_staff.level = ""
        user.user_staff.save(update_fields=['level'])
        UserWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
    except:
        pass

def remove_user_moderator(user, request_user):
    try:
        user.user_staff.level = ""
        user.user_staff.save(update_fields=['level'])
        UserWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_manager_state()
    except:
        pass

def remove_user_editor(user, request_user):
    try:
        user.user_staff.level = ""
        user.user_staff.save(update_fields=['level'])
        UserWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass

def remove_user_advertiser(user, request_user):
    try:
        user.user_staff.level = ""
        user.user_staff.save(update_fields=['level'])
        UserWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADVERTISER)
        check_manager_state()
    except:
        pass


def add_user_administrator_worker(user, request_user):
    try:
        user.can_work_staff_user.is_administrator = True
        user.can_work_staff_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffUser.objects.create(user=user, is_administrator=True)
    user.is_supermanager = True
    UserCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_user_moderator_worker(user, request_user):
    try:
        user.can_work_staff_user.is_moderator = True
        user.can_work_staff_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffUser.objects.create(user=user, is_moderator=True)
    user.is_supermanager = True
    UserCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_user_editor_worker(user, request_user):
    try:
        user.can_work_staff_user.is_editor = True
        user.can_work_staff_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffUser.objects.create(user=user, is_editor=True)
    user.is_supermanager = True
    UserCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def add_user_advertiser_worker(user, request_user):
    try:
        user.can_work_staff_user.is_advertiser = True
        user.can_work_staff_user.save(update_fields=['is_advertiser'])
    except:
        user_staff = CanWorkStaffUser.objects.create(user=user, is_advertiser=True)
    user.is_supermanager = True
    UserCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_user_administrator_worker(user, request_user):
    try:
        user.can_work_staff_user.is_administrator = False
        user.can_work_staff_user.save(update_fields=['is_administrator'])
        UserCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_user_moderator_worker(user, request_user):
    try:
        user.can_work_staff_user.is_moderator = False
        user.can_work_staff_user.save(update_fields=['is_moderator'])
        UserCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_user_editor_worker(user, request_user):
    try:
        user.can_work_staff_user.is_editor = False
        user.can_work_staff_user.save(update_fields=['is_editor'])
        UserCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass

def remove_user_advertiser_worker(user, request_user):
    try:
        user.can_work_staff_user.is_advertiser = False
        user.can_work_staff_user.save(update_fields=['is_advertiser'])
        UserCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADVERTISER)
        check_supermanager_state()
    except:
        pass
