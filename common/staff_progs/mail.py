from managers.models import MailUserStaff, CanWorkStaffMailUser
from logs.model.manage_mail import MailWorkerManageLog, MailCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state
from users.models import User


def add_mail_administrator(user, request_user):
    try:
        user.mail_user_staff.level = "A"
        user.mail_user_staff.save(update_fields=['level'])
    except:
        user_staff = MailUserStaff.objects.create(user=user, level="A")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    MailWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_mail_moderator(user, request_user):
    try:
        user.mail_user_staff.level = "M"
        user.mail_user_staff.save(update_fields=['level'])
    except:
        user_staff = MailUserStaff.objects.create(user=user, level="M")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    MailWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_mail_editor(user, request_user):
    try:
        user.mail_user_staff.level = "E"
        user.mail_user_staff.save(update_fields=['level'])
    except:
        user_staff = MailUserStaff.objects.create(user=user, level="E")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    MailWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_mail_administrator(user, request_user):
    try:
        user.mail_user_staff.level = ""
        user.mail_user_staff.save(update_fields=['level'])
        MailWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_mail_moderator(user, request_user):
    try:
        user.mail_user_staff.level = ""
        user.mail_user_staff.save(update_fields=['level'])
        check_manager_state()
        MailWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
    except:
        pass

def remove_mail_editor(user, request_user):
    try:
        user.mail_user_staff.level = ""
        user.mail_user_staff.save(update_fields=['level'])
        MailWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_mail_administrator_worker(user, request_user):
    try:
        user.can_work_staff_mail_user.is_administrator = True
        user.can_work_staff_mail_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffMail.objects.create(user=user, is_administrator=True)
    user.is_supermanager = True
    MailCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_mail_moderator_worker(user, request_user):
    try:
        user.can_work_staff_mail_user.is_moderator = True
        user.can_work_staff_mail_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffMail.objects.create(user=user, is_moderator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    MailCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_mail_editor_worker(user, request_user):
    try:
        user.can_work_staff_mail_user.is_editor = True
        user.can_work_staff_mail_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffMail.objects.create(user=user, is_editor=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    MailCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_mail_administrator_worker(user, request_user):
    try:
        user.can_work_staff_mail_user.is_administrator = False
        user.can_work_staff_mail_user.save(update_fields=['is_administrator'])
        MailCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_mail_moderator_worker(user, request_user):
    try:
        user.can_work_staff_mail_user.is_moderator = False
        user.can_work_staff_mail_user.save(update_fields=['is_moderator'])
        MailCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_mail_editor_worker(user, request_user):
    try:
        user.can_work_staff_mail_user.is_editor = False
        user.can_work_staff_mail_user.save(update_fields=['is_editor'])
        MailCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
