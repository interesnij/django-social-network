from managers.models import GoodUserStaff, CanWorkStaffGoodUser
from logs.model.manage_goods import GoodWorkerManageLog, GoodCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state
from users.models import User


def add_good_administrator(user, request_user):
    try:
        user.good_user_staff.level = "A"
        user.good_user_staff.save(update_fields=['level'])
    except:
        user_staff = GoodStaff.objects.create(user=user, level="A")
    user.perm = User.MANAGER
    user.save(update_fields=['perm'])
    GoodWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_good_moderator(user, request_user):
    try:
        user.good_user_staff.level = "M"
        user.good_user_staff.save(update_fields=['level'])
    except:
        user_staff = GoodStaff.objects.create(user=user, level="M")
    user.perm = User.MANAGER
    user.save(update_fields=['perm'])
    GoodWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_good_editor(user, request_user):
    try:
        user.good_user_staff.level = "E"
        user.good_user_staff.save(update_fields=['level'])
    except:
        user_staff = GoodStaff.objects.create(user=user, level="E")
    user.perm = User.MANAGER
    user.save(update_fields=['perm'])
    GoodWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_good_administrator(user, request_user):
    try:
        user.good_user_staff.level = ""
        user.good_user_staff.save(update_fields=['level'])
        GoodWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_post_moderator(user, request_user):
    try:
        user.good_user_staff.level = ""
        user.good_user_staff.save(update_fields=['level'])
        GoodWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_manager_state()
    except:
        pass

def remove_good_editor(user, request_user):
    try:
        user.good_user_staff.level = ""
        user.good_user_staff.save(update_fields=['level'])
        GoodWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_good_administrator_worker(user, request_user):
    try:
        user.can_work_staff_good_user.is_administrator = True
        user.can_work_staff_good_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffGood.objects.create(user=user, is_administrator=True)
    user.perm = User.SUPERMANAGER
    user.save(update_fields=['perm'])
    GoodCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_good_moderator_worker(user, request_user):
    try:
        user.can_work_staff_good_user.is_moderator = True
        user.can_work_staff_good_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffGood.objects.create(user=user, is_moderator=True)
    user.perm = User.SUPERMANAGER
    user.save(update_fields=['perm'])
    GoodCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_good_editor_worker(user, request_user):
    try:
        user.can_work_staff_good_user.is_editor = True
        user.can_work_staff_good_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffGood.objects.create(user=user, is_editor=True)
    user.perm = User.SUPERMANAGER
    user.save(update_fields=['perm'])
    GoodCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_good_administrator_worker(user, request_user):
    try:
        user.can_work_staff_good_user.is_administrator = False
        user.can_work_staff_good_user.save(update_fields=['is_administrator'])
        GoodCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_good_moderator_worker(user, request_user):
    try:
        user.can_work_staff_good_user.is_moderator = False
        user.can_work_staff_good_user.save(update_fields=['is_moderator'])
        GoodCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_good_editor_worker(user, request_user):
    try:
        user.can_work_staff_good_user.is_editor = False
        user.can_work_staff_good_user.save(update_fields=['is_editor'])
        GoodCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
