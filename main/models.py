import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.indexes import BrinIndex
from django.db import transaction
from notifications.models import Notification, notification_handler
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q
from django.db.models import Count
from common.models import Emoji


class Item(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    #community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")
    is_edited = models.BooleanField(default=False, verbose_name="Изменено")
    is_closed = models.BooleanField(default=False, verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    is_repost = models.BooleanField(verbose_name="Это репост", default=False)
    views=models.IntegerField(default=0, verbose_name="Просмотры")
    #moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='items')
    parent = models.ForeignKey("self", blank=True,
        null=True, on_delete=models.CASCADE, related_name="thread")
    STATUS_DRAFT = 'D'
    STATUS_PROCESSING = 'PG'
    STATUS_PUBLISHED = 'P'
    STATUS_ARHIVED = 'A'
    STATUSES = (
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PROCESSING, 'Обработка'),
        (STATUS_PUBLISHED, 'Опубликована'),
        (STATUS_ARHIVED, 'Архивирована'),
    )
    status = models.CharField(blank=False, null=False, choices=STATUSES, default=STATUS_DRAFT, max_length=2, verbose_name="Статус статьи")

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )

        ordering = ['-id']
        verbose_name="запись"
        verbose_name_plural="записи"

    def save(self, *args, **kwargs):
        if not self.is_fixed:
            return super(Item, self).save(*args, **kwargs)
        with transaction.atomic():
            Item.objects.filter(
                is_fixed=True).update(is_fixed=False)
            return super(Item, self).save(*args, **kwargs)

    def count_comments(self):
        parent_comments = ItemComment.objects.filter(item=self).count()
        return parent_comments

    def get_replies(self):
        get_comments = ItemComment.objects.filter(parent_comment=self).all()
        return get_comments

    def get_parent(self):
        if self.parent:
            return self.parent
        else:
            return self

    def get_thread(self):
        parent = self.get_parent()
        return parent.thread.all()

    def count_thread(self):
        return self.get_thread().count()

    def __str__(self):
        return "{0}/{1}".format(self.creator.get_full_name(), self.views)

    def notification_repost(self, user):
        notification_handler(user, self.creator,Notification.REPOST, action_object=self,id_value=str(self.uuid),key='social_update')

    def get_emoji_for_post(self, emoji_id=None, reactor_id=None):
        return Emoji.get_emoji(item_id=self, emoji_id=emoji_id, reactor_id=reactor_id)

    @classmethod
    def count_reactions_for_post_with_id(cls, post_id, reactor_id=None):
        count_query = Q(post_id=post_id, reactor__is_deleted=False)

        if reactor_id:
            count_query.add(Q(reactor_id=reactor_id), Q.AND)

        return cls.objects.filter(count_query).count()


class ItemComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def notification_comment(self, user):
        notification_handler(user, self.commenter,Notification.POST_COMMENT, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_reply_comment(self, user):
        notification_handler(user, self.commenter,Notification.POST_COMMENT_REPLY, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_comment_react(self, user):
        notification_handler(user, self.reactor,Notification.REACT_COMMENT, action_object=self,id_value=str(self.uuid),key='social_update')

    def get_emoji_for_post_comment(self, emoji_id=None, reactor_id=None):
        return Emoji.get_emoji_comment(post_comment_id=self, emoji_id=emoji_id,
                                                               reactor_id=reactor_id)



class ItemReaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reactions')
    created = models.DateTimeField(editable=False)
    reactor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_reactions')
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='post_reactions')

    class Meta:
        unique_together = ('reactor', 'item', 'emoji')
        verbose_name="реакция к записи"
        verbose_name_plural="реакции к записям"

    @classmethod
    def count_reactions_for_post_with_id(cls, item, reactor_id=None):
        count_query = Q(item=item, reactor__is_deleted=False)

        if reactor_id:
            count_query.add(Q(reactor_id=reactor_id), Q.AND)

        return cls.objects.filter(count_query).count()

    def __str__(self):
        return "{0}/{1}".format(self.item.creator.get_full_name(), self.emoji.keyword)

    def get_reactor(self):
        reactors = User.objects.filter(pk=self.reactor.pk).all()
        return reactors

    def notification_react(self, user):
        notification_handler(user, self.reactor,Notification.REACT, action_object=self,id_value=str(self.id),key='social_update')


class ItemCommentReaction(models.Model):
    item_comment = models.ForeignKey(ItemComment, on_delete=models.CASCADE, related_name='reactions')
    created = models.DateTimeField(editable=False)
    reactor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_reactions')
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='post_comment_reactions')

    class Meta:
        unique_together = ('reactor', 'item_comment','emoji')
        verbose_name="реакция на комментарий"
        verbose_name_plural="реакции на комментарии"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(ItemCommentReaction, self).save(*args, **kwargs)


class ItemMute(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='mutes')
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_mutes')

    class Meta:
        unique_together = ('item', 'muter',)

    @classmethod
    def create_post_mute(cls, item_id, muter_id):
        return cls.objects.create(item_id=item_id, muter_id=muter_id)


class ItemCommentMute(models.Model):
    item_comment = models.ForeignKey(ItemComment, on_delete=models.CASCADE, related_name='mutes')
    muter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_mutes')

    class Meta:
        unique_together = ('item_comment', 'muter',)

    @classmethod
    def create_post_comment_mute(cls, post_comment_id, muter_id):
        return cls.objects.create(post_comment_id=post_comment_id, muter_id=muter_id)


class TopPost(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='top_post')
    created = models.DateTimeField(editable=False, db_index=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()

        return super(TopPost, self).save(*args, **kwargs)
