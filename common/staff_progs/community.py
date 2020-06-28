from managers.models import CommunityStaff, CanWorkStaffCommunity
from logs.model.user_community import CommunityWorkerManageLog, CommunityCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state


def add_community_administrator(user, request_user):
    try:
        user.user_community_staff.level = "A"
        user.user_community_staff.save(update_fields=['level'])
    except:
        user_staff = CommunityStaff.objects.create(user=user, level="A")
    user.is_manager = True
    CommunityWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_community_moderator(user, request_user):
    try:
        user.user_community_staff.level = "M"
        user.user_community_staff.save(update_fields=['level'])
    except:
        user_staff = CommunityStaff.objects.create(user=user, level="M")
    user.is_manager = True
    CommunityWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_community_editor(user, request_user):
    try:
        user.user_community_staff.level = "E"
        user.user_community_staff.save(update_fields=['level'])
    except:
        user_staff = CommunityStaff.objects.create(user=user, level="E")
    user.is_manager = True
    CommunityWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def add_community_advertiser(user, request_user):
    try:
        user.user_community_staff.level = "R"
        user.user_community_staff.save(update_fields=['level'])
    except:
        user_staff = CommunityStaff.objects.create(user=user, level="R")
    user.is_manager = True
    CommunityWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_community_administrator(user, request_user):
    try:
        user.user_community_staff.level = ""
        user.user_community_staff.save(update_fields=['level'])
        CommunityWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_community_moderator(user, request_user):
    try:
        user.user_community_staff.level = ""
        user.user_community_staff.save(update_fields=['level'])
        CommunityWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_manager_state()
    except:
        pass

def remove_community_editor(user, request_user):
    try:
        user.user_community_staff.level = ""
        user.user_community_staff.save(update_fields=['level'])
        CommunityWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass

def remove_community_advertiser(user, request_user):
    try:
        user.user_community_staff.level = ""
        user.user_community_staff.save(update_fields=['level'])
        CommunityWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADVERTISER)
        check_manager_state()
    except:
        pass


def add_community_administrator_worker(user, request_user):
    try:
        user.can_work_staff_community.is_administrator = True
        user.can_work_staff_community.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffCommunity.objects.create(user=user, is_administrator=True)
    user.is_supermanager = True
    CommunityCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_community_moderator_worker(user, request_user):
    try:
        user.can_work_staff_community.is_moderator = True
        user.can_work_staff_community.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffCommunity.objects.create(user=user, is_moderator=True)
    user.is_supermanager = True
    CommunityCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_community_editor_worker(user, request_user):
    try:
        user.can_work_staff_community.is_editor = True
        user.can_work_staff_community.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffCommunity.objects.create(user=user, is_editor=True)
    user.is_supermanager = True
    CommunityCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def add_community_advertiser_worker(user, request_user):
    try:
        user.can_work_staff_community.is_advertiser = True
        user.can_work_staff_community.save(update_fields=['is_advertiser'])
    except:
        user_staff = CanWorkStaffCommunity.objects.create(user=user, is_advertiser=True)
    user.is_supermanager = True
    CommunityCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_community_administrator_worker(user, request_user):
    try:
        user.can_work_staff_community.is_administrator = False
        user.can_work_staff_community.save(update_fields=['is_administrator'])
        CommunityCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_community_moderator_worker(user, request_user):
    try:
        user.can_work_staff_community.is_moderator = False
        user.can_work_staff_community.save(update_fields=['is_moderator'])
        CommunityCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_community_editor_worker(user, request_user):
    try:
        user.can_work_staff_community.is_editor = False
        user.can_work_staff_community.save(update_fields=['is_editor'])
        CommunityCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass

def remove_community_advertiser_worker(user, request_user):
    try:
        user.can_work_staff_community.is_advertiser = False
        user.can_work_staff_community.save(update_fields=['is_advertiser'])
        CommunityCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADVERTISER)
        check_supermanager_state()
    except:
        pass
