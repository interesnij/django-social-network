from managers.models import DocUserStaff, CanWorkStaffDocUser
from logs.model.manage_doc import DocWorkerManageLog, DocCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state
from users.models import User


def add_doc_administrator(user, request_user):
    try:
        user.doc_user_staff.level = "A"
        user.doc_user_staff.save(update_fields=['level'])
    except:
        user_staff = DocUserStaff.objects.create(user=user, level="A")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    DocWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_doc_moderator(user, request_user):
    try:
        user.doc_user_staff.level = "M"
        user.doc_user_staff.save(update_fields=['level'])
    except:
        user_staff = DocUserStaff.objects.create(user=user, level="M")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    DocWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_doc_editor(user, request_user):
    try:
        user.doc_user_staff.level = "E"
        user.doc_user_staff.save(update_fields=['level'])
    except:
        user_staff = DocUserStaff.objects.create(user=user, level="E")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    DocWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_doc_administrator(user, request_user):
    try:
        user.doc_user_staff.level = ""
        user.doc_user_staff.save(update_fields=['level'])
        DocWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_doc_moderator(user, request_user):
    try:
        user.doc_user_staff.level = ""
        user.doc_user_staff.save(update_fields=['level'])
        check_manager_state()
        DocWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
    except:
        pass

def remove_doc_editor(user, request_user):
    try:
        user.doc_user_staff.level = ""
        user.doc_user_staff.save(update_fields=['level'])
        DocWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_doc_administrator_worker(user, request_user):
    try:
        user.can_work_staff_doc_user.is_administrator = True
        user.can_work_staff_doc_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffDoc.objects.create(user=user, is_administrator=True)
    user.is_supermanager = True
    DocCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_doc_moderator_worker(user, request_user):
    try:
        user.can_work_staff_doc_user.is_moderator = True
        user.can_work_staff_doc_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffDoc.objects.create(user=user, is_moderator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    DocCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_doc_editor_worker(user, request_user):
    try:
        user.can_work_staff_doc_user.is_editor = True
        user.can_work_staff_doc_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffDoc.objects.create(user=user, is_editor=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    DocCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_doc_administrator_worker(user, request_user):
    try:
        user.can_work_staff_doc_user.is_administrator = False
        user.can_work_staff_doc_user.save(update_fields=['is_administrator'])
        DocCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_doc_moderator_worker(user, request_user):
    try:
        user.can_work_staff_doc_user.is_moderator = False
        user.can_work_staff_doc_user.save(update_fields=['is_moderator'])
        DocCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_doc_editor_worker(user, request_user):
    try:
        user.can_work_staff_doc_user.is_editor = False
        user.can_work_staff_doc_user.save(update_fields=['is_editor'])
        DocCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
