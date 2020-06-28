from managers.models import PhotoUserStaff, CanWorkStaffPhotoUser
from logs.model.photo import PhotoWorkerManageLog, PhotoCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state


def add_photo_administrator(user, request_user):
    try:
        user.photo_user_staff.level = "A"
        user.photo_user_staff.save(update_fields=['level'])
    except:
        user_staff = PhotoStaff.objects.create(user=user, level="A")
    PhotoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_photo_moderator(user, request_user):
    try:
        user.photo_user_staff.level = "M"
        user.photo_user_staff.save(update_fields=['level'])
    except:
        user_staff = PhotoStaff.objects.create(user=user, level="M")
    PhotoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_photo_editor(user, request_user):
    try:
        user.photo_user_staff.level = "E"
        user.photo_user_staff.save(update_fields=['level'])
    except:
        user_staff = PhotoStaff.objects.create(user=user, level="E")
    PhotoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_photo_administrator(user, request_user):
    try:
        user.photo_user_staff.level = ""
        user.photo_user_staff.save(update_fields=['level'])
        PhotoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_photo_moderator(user, request_user):
    try:
        user.photo_user_staff.level = ""
        user.photo_user_staff.save(update_fields=['level'])
        PhotoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_manager_state()
    except:
        pass

def remove_photo_editor(user, request_user):
    try:
        user.photo_user_staff.level = ""
        user.photo_user_staff.save(update_fields=['level'])
        PhotoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_photo_administrator_worker(user, request_user):
    try:
        user.can_work_staff_photo_user.is_administrator = True
        user.can_work_staff_photo_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffPhoto.objects.create(user=user, is_administrator=True)
    PhotoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_photo_moderator_worker(user, request_user):
    try:
        user.can_work_staff_photo_user.is_moderator = True
        user.can_work_staff_photo_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffPhoto.objects.create(user=user, is_moderator=True)
    PhotoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_photo_editor_worker(user, request_user):
    try:
        user.can_work_staff_photo_user.is_editor = True
        user.can_work_staff_photo_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffPhoto.objects.create(user=user, is_editor=True)
    PhotoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_photo_administrator_worker(user, request_user):
    try:
        user.can_work_staff_photo_user.is_administrator = False
        user.can_work_staff_photo_user.save(update_fields=['is_administrator'])
        PhotoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_photo_moderator_worker(user, request_user):
    try:
        user.can_work_staff_photo_user.is_moderator = False
        user.can_work_staff_photo_user.save(update_fields=['is_moderator'])
        PhotoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_photo_editor_worker(user, request_user):
    try:
        user.can_work_staff_photo_user.is_editor = False
        user.can_work_staff_photo_user.save(update_fields=['is_editor'])
        PhotoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
