from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from users.models import User



class ModerationCategory(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False,verbose_name="Название")
    title = models.CharField(max_length=64, blank=False, null=False,verbose_name="Заголовок")
    description = models.CharField(max_length=255, blank=False, null=False,verbose_name="Описание")
    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True,verbose_name="Создано")
    order = models.PositiveSmallIntegerField(editable=False,verbose_name="Порядковый номер")

    SEVERITY_CRITICAL = 'C'
    SEVERITY_HIGH = 'H'
    SEVERITY_MEDIUM = 'M'
    SEVERITY_LOW = 'L'
    SEVERITIES = (
        (SEVERITY_CRITICAL, 'Критический'),
        (SEVERITY_HIGH, 'Высокий'),
        (SEVERITY_MEDIUM, 'Средний'),
        (SEVERITY_LOW, 'Низкий'),
    )

    severity = models.CharField(max_length=5, choices=SEVERITIES,verbose_name="Строгость"),


class ModeratedObject(models.Model):
    #community = models.ForeignKey('communities.Community', on_delete=models.CASCADE,related_name='moderated_objects',null=True,blank=False,verbose_name="Сообщество")
    description = models.CharField(max_length=300,
                                   blank=False, null=True,verbose_name="Описание")
    verified = models.BooleanField(default=False,
                                   blank=False, null=False,verbose_name="Одобрено")

    STATUS_PENDING = 'P'
    STATUS_APPROVED = 'A'
    STATUS_REJECTED = 'R'

    STATUSES = (
        (STATUS_PENDING, 'На рассмотрении'),
        (STATUS_APPROVED, 'Одобренный'),
        (STATUS_REJECTED, 'Отвергнутый'),
    )

    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING,verbose_name="Статус")

    category = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='moderated_objects',verbose_name="Категория")

    OBJECT_TYPE_POST = 'P'
    OBJECT_TYPE_POST_COMMENT = 'PC'
    OBJECT_TYPE_COMMUNITY = 'C'
    OBJECT_TYPE_USER = 'U'
    OBJECT_TYPES = (
        (OBJECT_TYPE_POST, 'Пост'),
        (OBJECT_TYPE_POST_COMMENT, 'Комментарий к посту'),
        (OBJECT_TYPE_COMMUNITY, 'Общество'),
        (OBJECT_TYPE_USER, 'Пользователь'),
    )

    object_type = models.CharField(max_length=5, choices=OBJECT_TYPES,verbose_name="Тип модерируемого объекта")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class ModerationReport(models.Model):
    #reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_reports', null=False,verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedObject, on_delete=models.CASCADE, related_name='reports', null=False,verbose_name="Объект")
    category = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='reports', null=False,verbose_name="Категория")
    description = models.CharField(max_length=300,
                                   blank=False, null=True,verbose_name="Описание")


class ModerationPenalty(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_penalties',verbose_name="Оштрафованный пользователь")
    expiration = models.DateTimeField(null=True,verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedObject, on_delete=models.CASCADE, related_name='user_penalties',verbose_name="Объект")

    TYPE_SUSPENSION = 'S'

    TYPES = (
        (TYPE_SUSPENSION, 'Приостановлено'),
    )

    type = models.CharField(max_length=5, choices=TYPES,verbose_name="Тип")


class ModeratedObjectLog(models.Model):
    #actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True,verbose_name="инициатор")

    LOG_TYPE_DESCRIPTION_CHANGED = 'DC'
    LOG_TYPE_STATUS_CHANGED = 'AC'
    LOG_TYPE_VERIFIED_CHANGED = 'VC'
    LOG_TYPE_CATEGORY_CHANGED = 'CC'

    LOG_TYPES = (
        (LOG_TYPE_DESCRIPTION_CHANGED, 'Описание Изменено'),
        (LOG_TYPE_STATUS_CHANGED, 'Статус Изменился'),
        (LOG_TYPE_VERIFIED_CHANGED, 'Проверка Изменена'),
        (LOG_TYPE_CATEGORY_CHANGED, 'Категория изменена'),
    )

    log_type = models.CharField(max_length=5, choices=LOG_TYPES,verbose_name="Тип")

    # Общие типы отношений
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    moderated_object = models.ForeignKey(ModeratedObject, on_delete=models.CASCADE, related_name='logs',verbose_name="Объект")
    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True,verbose_name="Создан")


class ModeratedObjectCategoryChangedLog(models.Model):
    log = GenericRelation(ModeratedObjectLog)
    changed_from = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='+',verbose_name="От")
    changed_to = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='+',verbose_name="До")



class ModeratedObjectDescriptionChangedLog(models.Model):
    log = GenericRelation(ModeratedObjectLog)
    changed_from = models.CharField(max_length=100,
                                    blank=False, null=True,verbose_name="От")
    changed_to = models.CharField(max_length=100,blank=False, null=True,verbose_name="До")

    @classmethod
    def create_moderated_object_description_changed_log(cls, moderated_object_id, changed_from, changed_to, actor_id):
        moderated_object_description_changed_log = cls.objects.create(changed_from=changed_from,
                                                                      changed_to=changed_to)
        ModeratedObjectLog.create_moderated_object_log(log_type=ModeratedObjectLog.LOG_TYPE_DESCRIPTION_CHANGED,
                                                       content_object=moderated_object_description_changed_log,
                                                       moderated_object_id=moderated_object_id,
                                                       actor_id=actor_id)



class ModeratedObjectStatusChangedLog(models.Model):
    log = GenericRelation(ModeratedObjectLog)
    changed_from = models.CharField(choices=ModeratedObject.STATUSES,
                                    blank=False, null=False, max_length=5,verbose_name="От")
    changed_to = models.CharField(blank=False, null=False, max_length=5,verbose_name="До")


class ModeratedObjectVerifiedChangedLog(models.Model):
    log = GenericRelation(ModeratedObjectLog)
    changed_from = models.BooleanField(blank=False, null=False,verbose_name="От")
    changed_to = models.BooleanField(blank=False, null=False,verbose_name="До")
