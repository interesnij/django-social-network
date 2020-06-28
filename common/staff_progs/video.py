from managers.models import VideoUserStaff, CanWorkStaffVideoUser
from logs.model.video import VideoWorkerManageLog, VideoCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state


def add_video_administrator(user, request_user):
    try:
        user.video_user_staff.level = "A"
        user.video_user_staff.save(update_fields=['level'])
    except:
        user_staff = VideoStaff.objects.create(user=user, level="A")
    user.is_manager = True
    VideoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_video_moderator(user, request_user):
    try:
        user.video_user_staff.level = "M"
        user.video_user_staff.save(update_fields=['level'])
    except:
        user_staff = VideoStaff.objects.create(user=user, level="M")
    user.is_manager = True
    VideoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_video_editor(user, request_user):
    try:
        user.video_user_staff.level = "E"
        user.video_user_staff.save(update_fields=['level'])
    except:
        user_staff = VideoStaff.objects.create(user=user, level="E")
    user.is_manager = True
    VideoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_video_administrator(user, request_user):
    try:
        user.video_user_staff.level = ""
        user.video_user_staff.save(update_fields=['level'])
        VideoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_video_moderator(user, request_user):
    try:
        user.video_user_staff.level = ""
        user.video_user_staff.save(update_fields=['level'])
        VideoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_manager_state()
    except:
        pass

def remove_video_editor(user, request_user):
    try:
        user.video_user_staff.level = ""
        user.video_user_staff.save(update_fields=['level'])
        VideoWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_video_administrator_worker(user, request_user):
    try:
        user.can_work_staff_video_user.is_administrator = True
        user.can_work_staff_video_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffVideo.objects.create(user=user, is_administrator=True)
    user.is_supermanager = True
    VideoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_video_moderator_worker(user, request_user):
    try:
        user.can_work_staff_video_user.is_moderator = True
        user.can_work_staff_video_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffVideo.objects.create(user=user, is_moderator=True)
    user.is_supermanager = True
    VideoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_video_editor_worker(user, request_user):
    try:
        user.can_work_staff_video_user.is_editor = True
        user.can_work_staff_video_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffVideo.objects.create(user=user, is_editor=True)
    user.is_supermanager = True
    VideoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_video_administrator_worker(user, request_user):
    try:
        user.can_work_staff_video_user.is_administrator = False
        user.can_work_staff_video_user.save(update_fields=['is_administrator'])
        VideoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_video_moderator_worker(user, request_user):
    try:
        user.can_work_staff_video_user.is_moderator = False
        user.can_work_staff_video_user.save(update_fields=['is_moderator'])
        VideoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_video_editor_worker(user, request_user):
    try:
        user.can_work_staff_video_user.is_editor = False
        user.can_work_staff_video_user.save(update_fields=['is_editor'])
        VideoCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
