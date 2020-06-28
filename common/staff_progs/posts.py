from managers.models import PostUserStaff, CanWorkStaffPostUser
from logs.model.posts import PostWorkerManageLog, PostCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state


def add_post_administrator(user, request_user):
    try:
        user.post_user_staff.level = "A"
        user.post_user_staff.save(update_fields=['level'])
    except:
        user_staff = PostStaff.objects.create(user=user, level="A")
    PostWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_post_moderator(user, request_user):
    try:
        user.post_user_staff.level = "M"
        user.post_user_staff.save(update_fields=['level'])
    except:
        user_staff = PostStaff.objects.create(user=user, level="M")
    PostWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_post_editor(user, request_user):
    try:
        user.post_user_staff.level = "E"
        user.post_user_staff.save(update_fields=['level'])
    except:
        user_staff = PostStaff.objects.create(user=user, level="E")
    PostWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_post_administrator(user, request_user):
    try:
        user.post_user_staff.level = ""
        user.post_user_staff.save(update_fields=['level'])
        PostWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_post_moderator(user, request_user):
    try:
        user.post_user_staff.level = ""
        user.post_user_staff.save(update_fields=['level'])
        PostWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_manager_state()
    except:
        pass

def remove_post_editor(user, request_user):
    try:
        user.post_user_staff.level = ""
        user.post_user_staff.save(update_fields=['level'])
        PostWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_post_administrator_worker(user, request_user):
    try:
        user.can_work_staff_post_user.is_administrator = True
        user.can_work_staff_post_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffPost.objects.create(user=user, is_administrator=True)
    PostCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_post_moderator_worker(user, request_user):
    try:
        user.can_work_staff_post_user.is_moderator = True
        user.can_work_staff_post_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffPost.objects.create(user=user, is_moderator=True)
    PostCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_post_editor_worker(user, request_user):
    try:
        user.can_work_staff_post_user.is_editor = True
        user.can_work_staff_post_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffPost.objects.create(user=user, is_editor=True)
    PostCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_post_administrator_worker(user, request_user):
    try:
        user.can_work_staff_post_user.is_administrator = False
        user.can_work_staff_post_user.save(update_fields=['is_administrator'])
        PostCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_post_moderator_worker(user, request_user):
    try:
        user.can_work_staff_post_user.is_moderator = False
        user.can_work_staff_post_user.save(update_fields=['is_moderator'])
        PostCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_post_editor_worker(user, request_user):
    try:
        user.can_work_staff_post_user.is_editor = False
        user.can_work_staff_post_user.save(update_fields=['is_editor'])
        PostCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
