from managers.models import ArticleUserStaff, CanWorkStaffArticleUser
from logs.model.manage_article import ArticleWorkerManageLog, ArticleCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state
from users.models import User


def add_article_administrator(user, request_user):
    try:
        user.article_user_staff.level = "A"
        user.article_user_staff.save(update_fields=['level'])
    except:
        user_staff = ArticleUserStaff.objects.create(user=user, level="A")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    ArticleWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_article_moderator(user, request_user):
    try:
        user.article_user_staff.level = "M"
        user.article_user_staff.save(update_fields=['level'])
    except:
        user_staff = ArticleUserStaff.objects.create(user=user, level="M")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    ArticleWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_article_editor(user, request_user):
    try:
        user.article_user_staff.level = "E"
        user.article_user_staff.save(update_fields=['level'])
    except:
        user_staff = ArticleUserStaff.objects.create(user=user, level="E")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    ArticleWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_article_administrator(user, request_user):
    try:
        user.article_user_staff.level = ""
        user.article_user_staff.save(update_fields=['level'])
        ArticleWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_article_moderator(user, request_user):
    try:
        user.article_user_staff.level = ""
        user.article_user_staff.save(update_fields=['level'])
        check_manager_state()
        ArticleWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
    except:
        pass

def remove_article_editor(user, request_user):
    try:
        user.article_user_staff.level = ""
        user.article_user_staff.save(update_fields=['level'])
        ArticleWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_article_administrator_worker(user, request_user):
    try:
        user.can_work_staff_article_user.is_administrator = True
        user.can_work_staff_article_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffArticle.objects.create(user=user, is_administrator=True)
    user.is_supermanager = True
    ArticleCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_article_moderator_worker(user, request_user):
    try:
        user.can_work_staff_article_user.is_moderator = True
        user.can_work_staff_article_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffArticle.objects.create(user=user, is_moderator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    ArticleCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_article_editor_worker(user, request_user):
    try:
        user.can_work_staff_article_user.is_editor = True
        user.can_work_staff_article_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffArticle.objects.create(user=user, is_editor=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    ArticleCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_article_administrator_worker(user, request_user):
    try:
        user.can_work_staff_article_user.is_administrator = False
        user.can_work_staff_article_user.save(update_fields=['is_administrator'])
        ArticleCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_article_moderator_worker(user, request_user):
    try:
        user.can_work_staff_article_user.is_moderator = False
        user.can_work_staff_article_user.save(update_fields=['is_moderator'])
        ArticleCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_article_editor_worker(user, request_user):
    try:
        user.can_work_staff_article_user.is_editor = False
        user.can_work_staff_article_user.save(update_fields=['is_editor'])
        ArticleCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
