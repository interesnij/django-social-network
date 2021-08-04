from managers.models import SiteUserStaff, CanWorkStaffSiteUser
from logs.model.manage_site import SiteWorkerManageLog, SiteCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state
from users.models import User


def add_site_administrator(user, request_user):
    try:
        user.site_user_staff.level = "A"
        user.site_user_staff.save(update_fields=['level'])
    except:
        user_staff = SiteUserStaff.objects.create(user=user, level="A")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    SiteWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_site_moderator(user, request_user):
    try:
        user.site_user_staff.level = "M"
        user.site_user_staff.save(update_fields=['level'])
    except:
        user_staff = SiteUserStaff.objects.create(user=user, level="M")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    SiteWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_site_editor(user, request_user):
    try:
        user.site_user_staff.level = "E"
        user.site_user_staff.save(update_fields=['level'])
    except:
        user_staff = SiteUserStaff.objects.create(user=user, level="E")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    SiteWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_site_administrator(user, request_user):
    try:
        user.site_user_staff.level = ""
        user.site_user_staff.save(update_fields=['level'])
        SiteWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_site_moderator(user, request_user):
    try:
        user.site_user_staff.level = ""
        user.site_user_staff.save(update_fields=['level'])
        check_manager_state()
        SiteWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
    except:
        pass

def remove_site_editor(user, request_user):
    try:
        user.site_user_staff.level = ""
        user.site_user_staff.save(update_fields=['level'])
        SiteWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_site_administrator_worker(user, request_user):
    try:
        user.can_work_staff_site_user.is_administrator = True
        user.can_work_staff_site_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffSite.objects.create(user=user, is_administrator=True)
    user.is_supermanager = True
    SiteCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_site_moderator_worker(user, request_user):
    try:
        user.can_work_staff_site_user.is_moderator = True
        user.can_work_staff_site_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffSite.objects.create(user=user, is_moderator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    SiteCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_site_editor_worker(user, request_user):
    try:
        user.can_work_staff_site_user.is_editor = True
        user.can_work_staff_site_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffSite.objects.create(user=user, is_editor=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    SiteCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_site_administrator_worker(user, request_user):
    try:
        user.can_work_staff_site_user.is_administrator = False
        user.can_work_staff_site_user.save(update_fields=['is_administrator'])
        SiteCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_site_moderator_worker(user, request_user):
    try:
        user.can_work_staff_site_user.is_moderator = False
        user.can_work_staff_site_user.save(update_fields=['is_moderator'])
        SiteCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_site_editor_worker(user, request_user):
    try:
        user.can_work_staff_site_user.is_editor = False
        user.can_work_staff_site_user.save(update_fields=['is_editor'])
        SiteCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
