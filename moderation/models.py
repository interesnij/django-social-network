from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from users.models import User
from posts.models import Post, PostComment
from article.models import Article, ArticleComment
from goods.models import Good, GoodComment



class ModerationCategory(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, verbose_name="Название")
    title = models.CharField(max_length=64, blank=False, null=False, verbose_name="Заголовок")
    description = models.CharField(max_length=255, blank=False, null=False, verbose_name="Описание")
    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создано")
    order = models.PositiveIntegerField(editable=False, verbose_name="Порядковый номер")

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

    severity = models.CharField(max_length=5, choices=SEVERITIES,verbose_name="Строгость")

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = timezone.now()
        return super(ModerationCategory, self).save(*args, **kwargs)


class ModeratedObject(models.Model):
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='moderated_objects', null=True, blank=False, verbose_name="Сообщество")
    description = models.CharField(max_length=300,
                                   blank=False, null=True, verbose_name="Описание")
    verified = models.BooleanField(default=False,
                                   blank=False, null=False, verbose_name="Одобрено")

    STATUS_PENDING = 'P'
    STATUS_APPROVED = 'A'
    STATUS_REJECTED = 'R'

    STATUSES = (
        (STATUS_PENDING, 'На рассмотрении'),
        (STATUS_APPROVED, 'Одобренный'),
        (STATUS_REJECTED, 'Отвергнутый'),
    )

    status = models.CharField(max_length=5, choices=STATUSES, default=STATUS_PENDING, verbose_name="Статус")

    category = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='moderated_objects', verbose_name="Категория")

    OBJECT_TYPE_POST = 'P'
    OBJECT_TYPE_POST_COMMENT = 'PC'
    OBJECT_TYPE_COMMUNITY = 'C'
    OBJECT_TYPE_USER = 'U'
    OBJECT_TYPE_ARTICLE = 'A'
    OBJECT_TYPE_ARTICLE_COMMENT = 'AC'
    OBJECT_TYPE_GOOD = 'G'
    OBJECT_TYPE_GOOD_COMMENT = 'GC'
    OBJECT_TYPES = (
        (OBJECT_TYPE_POST, 'Запись'),
        (OBJECT_TYPE_POST_COMMENT, 'Комментарий к запись'),
        (OBJECT_TYPE_COMMUNITY, 'Сообщество'),
        (OBJECT_TYPE_USER, 'Пользователь'),
        (OBJECT_TYPE_ARTICLE, 'Статья'),
        (OBJECT_TYPE_ARTICLE_COMMENT, 'Комментарий к статье'),
        (OBJECT_TYPE_GOOD, 'Товар'),
        (OBJECT_TYPE_GOOD_COMMENT, 'Комментарий к товару'),
    )

    object_type = models.CharField(max_length=5, choices=OBJECT_TYPES, verbose_name="Тип модерируемого объекта")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @classmethod
    def create_moderated_object(cls, object_type, content_object, category_id, community_id=None):
        """"
        Универсальный метод создания объекта модерации
        """
        return cls.objects.create(object_type=object_type, content_object=content_object, category_id=category_id,
                                  community_id=community_id)

    @classmethod
    def _get_or_create_moderated_object(cls, object_type, content_object, category_id, community_id=None):
        """"
        Универсальный метод получает объект модерации, если его нет-создает
        """
        try:
            moderated_object = cls.objects.get(object_type=object_type, object_id=content_object.pk,
                                               community_id=community_id)
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(object_type=object_type,
                                                           content_object=content_object, category_id=category_id,
                                                           community_id=community_id)

        return moderated_object

    @classmethod
    def get_or_create_moderated_object_for_post(cls, post, category_id):
        """"
        Создание или получение объекта модерации к записи
        """
        community_id = None

        if post.community:
            community_id = post.community.pk

        return cls._get_or_create_moderated_object(object_type=cls.OBJECT_TYPE_POST, content_object=post,
                                                   category_id=category_id, community_id=community_id)

    @classmethod
    def get_or_create_moderated_object_for_post_comment(cls, post_comment, category_id):
        """"
        Создание или получение объекта модерации к комментарию записи
        """
        community_id = None

        if post_comment.post.community:
            community_id = post_comment.post.community.pk

        return cls._get_or_create_moderated_object(object_type=cls.OBJECT_TYPE_POST_COMMENT,
                                                   content_object=post_comment,
                                                   category_id=category_id,
                                                   community_id=community_id)

    @classmethod
    def get_or_create_moderated_object_for_article(cls, article, category_id):
        """"
        Создание или получение объекта модерации к статье
        """
        community_id = None

        if article.community:
            community_id = article.community.pk

        return cls._get_or_create_moderated_object(object_type=cls.OBJECT_TYPE_ARTICLE, content_object=article,
                                                   category_id=category_id, community_id=community_id)

    @classmethod
    def get_or_create_moderated_object_for_article_comment(cls, article_comment, category_id):
        """"
        Создание или получение объекта модерации к комментрию статьи
        """
        community_id = None

        if article_comment.post.community:
            community_id = article_comment.article.community.pk

        return cls._get_or_create_moderated_object(object_type=cls.OBJECT_TYPE_ARTICLE_COMMENT,
                                                   content_object=article_comment,
                                                   category_id=category_id,
                                                   community_id=community_id)

    @classmethod
    def get_or_create_moderated_object_for_good(cls, good, category_id):
        """"
        Создание или получение объекта модерации к товару
        """
        community_id = None

        if good.community:
            community_id = good.community.pk

        return cls._get_or_create_moderated_object(object_type=cls.OBJECT_TYPE_GOOD, content_object=good,
                                                   category_id=category_id, community_id=community_id)

    @classmethod
    def get_or_create_moderated_object_for_good_comment(cls, good_comment, category_id):
        """"
        Создание или получение объекта модерации к комментрию товара
        """
        community_id = None

        if good_comment.good.community:
            community_id = good_comment.good.community.pk

        return cls._get_or_create_moderated_object(object_type=cls.OBJECT_TYPE_GOOD_COMMENT,
                                                   content_object=good_comment,
                                                   category_id=category_id,
                                                   community_id=community_id)

    @classmethod
    def get_or_create_moderated_object_for_community(cls, community, category_id):
        """"
        Создание или получение объекта модерации к сообществу
        """
        return cls._get_or_create_moderated_object(object_type=cls.OBJECT_TYPE_COMMUNITY, content_object=community,
                                                   category_id=category_id)

    @classmethod
    def get_or_create_moderated_object_for_user(cls, user, category_id):
        """"
        Создание или получение объекта модерации к пользователю
        """
        return cls._get_or_create_moderated_object(object_type=cls.OBJECT_TYPE_USER, content_object=user,
                                                   category_id=category_id)

    @property
    def reports_count(self):
        return self.reports.count()

    def is_verified(self):
        return self.verified

    def is_approved(self):
        return self.status == ModeratedObject.STATUS_APPROVED

    def is_pending(self):
        return self.status == ModeratedObject.STATUS_PENDING

    def update_with_actor_with_id(self, actor_id, description, category_id):
        if description is not None:
            current_description = self.description
            self.description = description
            ModeratedObjectDescriptionChangedLog.create_moderated_object_description_changed_log(
                changed_from=current_description, changed_to=description, moderated_object_id=self.pk,
                actor_id=actor_id)

        if category_id is not None:
            current_category_id = self.category_id
            self.category_id = category_id
            ModeratedObjectCategoryChangedLog.create_moderated_object_category_changed_log(
                changed_from_id=current_category_id, changed_to_id=category_id, moderated_object_id=self.pk,
                actor_id=actor_id)

        self.save()

    def verify_with_actor_with_id(self, actor_id):
        current_verified = self.verified
        self.verified = True
        ModeratedObjectVerifiedChangedLog.create_moderated_object_verified_changed_log(
            changed_from=current_verified, changed_to=self.verified, moderated_object_id=self.pk, actor_id=actor_id)

        content_object = self.content_object
        moderation_severity = self.category.severity
        penalty_targets = None

        if self.is_approved():
            if isinstance(content_object, User):
                penalty_targets = [content_object]
            elif isinstance(content_object, Post):
                penalty_targets = [content_object.creator]
            elif isinstance(content_object, PostComment):
                penalty_targets = [content_object.commenter]
            elif isinstance(content_object, Article):
                penalty_targets = [content_object.creator]
            elif isinstance(content_object, ArticleComment):
                penalty_targets = [content_object.commenter]
            elif isinstance(content_object, Good):
                penalty_targets = [content_object.creator]
            elif isinstance(content_object, GoodComment):
                penalty_targets = [content_object.commenter]
            elif isinstance(content_object, Community):
                penalty_targets = content_object.get_staff_members()
            elif isinstance(content_object, ModeratedObject):
                penalty_targets = content_object.get_reporters()

            for penalty_target in penalty_targets:
                duration_of_penalty = None
                penalties_count = penalty_target.count_moderation_penalties_for_moderation_severity(
                    moderation_severity=moderation_severity) + 1

                if moderation_severity == ModerationCategory.SEVERITY_CRITICAL:
                    duration_of_penalty = timezone.timedelta(weeks=5000)
                elif moderation_severity == ModerationCategory.SEVERITY_HIGH:
                    duration_of_penalty = timezone.timedelta(days=penalties_count ** 4)
                elif moderation_severity == ModerationCategory.SEVERITY_MEDIUM:
                    duration_of_penalty = timezone.timedelta(hours=penalties_count ** 3)
                elif moderation_severity == ModerationCategory.SEVERITY_LOW:
                    duration_of_penalty = timezone.timedelta(minutes=penalties_count ** 2)

                moderation_expiration = timezone.now() + duration_of_penalty

                ModerationPenalty.create_suspension_moderation_penalty(moderated_object=self,
                                                                       user_id=penalty_target.pk,
                                                                       expiration=moderation_expiration)

            if (isinstance(content_object, Post) or isinstance(content_object, PostComment) or isinstance(
                    content_object,
                    Community)) or (
                    isinstance(content_object, User) and moderation_severity == ModerationCategory.SEVERITY_CRITICAL):
                content_object.soft_delete()

                if moderation_severity == ModerationCategory.SEVERITY_CRITICAL and isinstance(content_object, Post):
                    content_object.delete_media()

            if (isinstance(content_object, Article) or isinstance(content_object, ArticleComment) or isinstance(
                    content_object,
                    Community)) or (
                    isinstance(content_object, User) and moderation_severity == ModerationCategory.SEVERITY_CRITICAL):
                content_object.soft_delete()

                if moderation_severity == ModerationCategory.SEVERITY_CRITICAL and isinstance(content_object, Article):
                    content_object.delete_media()

            if (isinstance(content_object, Good) or isinstance(content_object, GoodComment) or isinstance(
                    content_object,
                    Community)) or (
                    isinstance(content_object, User) and moderation_severity == ModerationCategory.SEVERITY_CRITICAL):
                content_object.soft_delete()

                if moderation_severity == ModerationCategory.SEVERITY_CRITICAL and isinstance(content_object, Good):
                    content_object.delete_media()

        content_object.save()
        self.save()

    def unverify_with_actor_with_id(self, actor_id):
        current_verified = self.verified
        self.verified = False
        ModeratedObjectVerifiedChangedLog.create_moderated_object_verified_changed_log(
            changed_from=current_verified, changed_to=self.verified, moderated_object_id=self.pk, actor_id=actor_id)
        self.user_penalties.all().delete()
        content_object = self.content_object

        moderation_severity = self.category.severity

        if (isinstance(content_object, Post) or isinstance(content_object, PostComment) or isinstance(
                content_object,
                Community)) or (
                isinstance(content_object, User) and moderation_severity == ModerationCategory.SEVERITY_CRITICAL):
            content_object.unsoft_delete()
        if (isinstance(content_object, Article) or isinstance(content_object, ArticleComment) or isinstance(
                content_object,
                Community)) or (
                isinstance(content_object, User) and moderation_severity == ModerationCategory.SEVERITY_CRITICAL):
            content_object.unsoft_delete()
        if (isinstance(content_object, Good) or isinstance(content_object, GoodComment) or isinstance(
                content_object,
                Community)) or (
                isinstance(content_object, User) and moderation_severity == ModerationCategory.SEVERITY_CRITICAL):
            content_object.unsoft_delete()
        self.save()
        content_object.save()

    def approve_with_actor_with_id(self, actor_id):
        current_status = self.status
        self.status = ModeratedObject.STATUS_APPROVED
        ModeratedObjectStatusChangedLog.create_moderated_object_status_changed_log(
            changed_from=current_status, changed_to=self.status, moderated_object_id=self.pk, actor_id=actor_id)
        self.save()

    def reject_with_actor_with_id(self, actor_id):
        current_status = self.status
        self.status = ModeratedObject.STATUS_REJECTED
        ModeratedObjectStatusChangedLog.create_moderated_object_status_changed_log(
            changed_from=current_status, changed_to=self.status, moderated_object_id=self.pk, actor_id=actor_id)
        self.save()

    def get_reporters(self):
        return User.objects.filter(moderation_reports__moderated_object_id=self.pk).all()



class ModerationReport(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_reports', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(ModeratedObject, on_delete=models.CASCADE, related_name='reports', null=False, verbose_name="Объект")
    category = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='reports', null=False, verbose_name="Категория")
    description = models.CharField(max_length=300,
                                   blank=False, null=True,verbose_name="Описание")

    @classmethod
    def create_post_moderation_report(cls, reporter_id, post, category_id, description):
        moderated_object = ModeratedObject.get_or_create_moderated_object_for_post(
            post=post,
            category_id=category_id
        )
        post_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id,
                                                    description=description, moderated_object=moderated_object)
        return post_moderation_report

    @classmethod
    def create_post_comment_moderation_report(cls, reporter_id, post_comment, category_id, description):
        moderated_object = ModeratedObject.get_or_create_moderated_object_for_post_comment(
            post_comment=post_comment,
            category_id=category_id
        )
        post_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id,
                                                            description=description, moderated_object=moderated_object)
        return post_comment_moderation_report

    @classmethod
    def create_article_moderation_report(cls, reporter_id, article, category_id, description):
        moderated_object = ModeratedObject.get_or_create_moderated_object_for_article(
            article=article,
            category_id=category_id
        )
        article_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id,
                                                    description=description, moderated_object=moderated_object)
        return article_moderation_report

    @classmethod
    def create_article_comment_moderation_report(cls, reporter_id, article_comment, category_id, description):
        moderated_object = ModeratedObject.get_or_create_moderated_object_for_article_comment(
            article_comment=article_comment,
            category_id=category_id
        )
        article_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id,
                                                            description=description, moderated_object=moderated_object)
        return article_comment_moderation_report

    @classmethod
    def create_good_moderation_report(cls, reporter_id, good, category_id, description):
        moderated_object = ModeratedObject.get_or_create_moderated_object_for_good(
            good=good,
            category_id=category_id
        )
        good_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id,
                                                    description=description, moderated_object=moderated_object)
        return good_moderation_report

    @classmethod
    def create_good_comment_moderation_report(cls, reporter_id, good_comment, category_id, description):
        moderated_object = ModeratedObject.get_or_create_moderated_object_for_good_comment(
            good_comment=good_comment,
            category_id=category_id
        )
        good_comment_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id,
                                                            description=description, moderated_object=moderated_object)
        return good_comment_moderation_report

    @classmethod
    def create_user_moderation_report(cls, reporter_id, user, category_id, description):
        moderated_object = ModeratedObject.get_or_create_moderated_object_for_user(
            user=user,
            category_id=category_id
        )
        user_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id,
                                                    description=description, moderated_object=moderated_object)
        return user_moderation_report

    @classmethod
    def create_community_moderation_report(cls, reporter_id, community, category_id, description):
        moderated_object = ModeratedObject.get_or_create_moderated_object_for_community(
            community=community,
            category_id=category_id
        )
        community_moderation_report = cls.objects.create(reporter_id=reporter_id, category_id=category_id,
                                                         description=description, moderated_object=moderated_object)
        return community_moderation_report



class ModerationPenalty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_penalties', verbose_name="Оштрафованный пользователь")
    expiration = models.DateTimeField(null=True,verbose_name="Окончание")
    moderated_object = models.ForeignKey(ModeratedObject, on_delete=models.CASCADE, related_name='user_penalties', verbose_name="Объект")

    TYPE_SUSPENSION = 'S'
    TYPES = (
        (TYPE_SUSPENSION, 'Приостановлено'),
    )
    type = models.CharField(max_length=5, choices=TYPES,verbose_name="Тип")

    @classmethod
    def create_suspension_moderation_penalty(cls, user_id, moderated_object, expiration):
        return cls.objects.create(moderated_object=moderated_object, user_id=user_id, type=cls.TYPE_SUSPENSION,
                                  expiration=expiration)


class ModeratedObjectLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True, verbose_name="инициатор")

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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    moderated_object = models.ForeignKey(ModeratedObject, on_delete=models.CASCADE, related_name='logs', verbose_name="Объект")
    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True, verbose_name="Создан")

    @classmethod
    def create_moderated_object_log(cls, moderated_object_id, log_type, content_object, actor_id):
        return cls.objects.create(log_type=log_type, content_object=content_object,
                                  moderated_object_id=moderated_object_id,
                                  actor_id=actor_id)

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = timezone.now()
        return super(ModeratedObjectLog, self).save(*args, **kwargs)


class ModeratedObjectCategoryChangedLog(models.Model):
    log = GenericRelation(ModeratedObjectLog)
    changed_from = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='+', verbose_name="От")
    changed_to = models.ForeignKey(ModerationCategory, on_delete=models.CASCADE, related_name='+', verbose_name="До")

    @classmethod
    def create_moderated_object_category_changed_log(cls, moderated_object_id, changed_from_id, changed_to_id,
                                                     actor_id):
        moderated_object_category_changed_log = cls.objects.create(changed_from_id=changed_from_id,
                                                                   changed_to_id=changed_to_id)
        ModeratedObjectLog.create_moderated_object_log(log_type=ModeratedObjectLog.LOG_TYPE_CATEGORY_CHANGED,
                                                       content_object=moderated_object_category_changed_log,
                                                       moderated_object_id=moderated_object_id, actor_id=actor_id)



class ModeratedObjectDescriptionChangedLog(models.Model):
    log = GenericRelation(ModeratedObjectLog)
    changed_from = models.CharField(max_length=100,
                                    blank=False, null=True, verbose_name="От")
    changed_to = models.CharField(max_length=100,blank=False, null=True, verbose_name="До")

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
                                    blank=False, null=False, max_length=5, verbose_name="От")
    changed_to = models.CharField(blank=False, null=False, max_length=5, verbose_name="До")

    @classmethod
    def create_moderated_object_status_changed_log(cls, moderated_object_id, changed_from, changed_to, actor_id):
        moderated_object_description_changed_log = cls.objects.create(changed_from=changed_from,
                                                                      changed_to=changed_to)
        ModeratedObjectLog.create_moderated_object_log(log_type=ModeratedObjectLog.LOG_TYPE_STATUS_CHANGED,
                                                       content_object=moderated_object_description_changed_log,
                                                       moderated_object_id=moderated_object_id, actor_id=actor_id)


class ModeratedObjectVerifiedChangedLog(models.Model):
    log = GenericRelation(ModeratedObjectLog)
    changed_from = models.BooleanField(blank=False, null=False, verbose_name="От")
    changed_to = models.BooleanField(blank=False, null=False, verbose_name="До")

    @classmethod
    def create_moderated_object_verified_changed_log(cls, moderated_object_id, changed_from, changed_to, actor_id):
        moderated_object_description_changed_log = cls.objects.create(changed_from=changed_from,
                                                                      changed_to=changed_to)
        ModeratedObjectLog.create_moderated_object_log(log_type=ModeratedObjectLog.LOG_TYPE_VERIFIED_CHANGED,
                                                       content_object=moderated_object_description_changed_log,
                                                       moderated_object_id=moderated_object_id, actor_id=actor_id)
