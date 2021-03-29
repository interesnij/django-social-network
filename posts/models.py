import uuid
from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from common.utils import try_except


class PostList(models.Model):
    MAIN, LIST, PRIVATE, DELETED, FIX = 'MA', 'LI', 'PR', 'DE', 'FI'
    TYPE = (
        (MAIN, 'Основной список'),
        (LIST, 'Пользовательский список'),
		(PRIVATE, 'Приватный список'),
		(DELETED, 'Архивный список'),
        (FIX, 'Закрепленный список'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_postlist', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_postlist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=5, choices=TYPE, default=LIST, verbose_name="Тип листа")
    order = models.PositiveIntegerField(default=1)
    is_deleted = models.BooleanField(verbose_name="Удален", default=False)

    def __str__(self):
        return self.name + " - " + self.creator.get_full_name()

    def is_post_in_list(self, post_id):
        return self.post_list.filter(pk=post_id).values("pk").exists()

    def is_not_empty(self):
        return self.post_list.filter(list=self).values("pk").exists()

    def get_posts(self):
        select_related = ('creator', 'community')
        only = ('creator__id', 'community__id', 'created')
        posts = self.post_list.select_related(*select_related).only(*only).filter(list=self, is_deleted=False, status="P").order_by("-created")
        return posts

    def list_30(self):
        queryset = self.post_list.only("pk")[:30].order_by('-created')
        return queryset
    def list_6(self):
        queryset = self.post_list.only("pk")[:6].order_by('-created')
        return queryset

    def count_posts(self):
        return self.post_list.filter(is_deleted=False).values("pk").count()
    def get_posts_ids(self):
        ids =  self.post_list.filter(is_deleted=False).values("pk")
        return [id['pk'] for id in ids]

    def is_full_list(self):
        if self.is_fix_list() and self.count_posts() == 10:
            return True
        else:
            return False

    def is_main_list(self):
        return self.type == self.MAIN
    def is_fix_list(self):
        return self.type == self.FIX
    def is_list_list(self):
        return self.type == self.LIST
    def is_deleted_list(self):
        return self.type == self.DELETED
    def is_private_list(self):
        return self.type == self.PRIVATE
    def is_user_list(self):
        if self.type == self.LIST or self.type == self.PRIVATE:
            return True
        else:
            return False

    class Meta:
        verbose_name = "список записей"
        verbose_name_plural = "списки записей"
        ordering = ['order']


class PostCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Тематика")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Тематика постов"
		verbose_name_plural = "Тематики постов"


class Post(models.Model):
    STATUS_DRAFT, STATUS_PROCESSING, STATUS_MESSAGE_PUBLISHED, STATUS_PUBLISHED = 'D', 'PG', 'MP', 'P'
    STATUSES = (
        (STATUS_DRAFT,'Черновик'),(STATUS_PROCESSING,'Обработка'),(STATUS_PUBLISHED,'Опубликована'),(STATUS_MESSAGE_PUBLISHED,'Репост в сообщения'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")

    community = models.ForeignKey('communities.Community', related_name='post_community', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщество")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="thread")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='post_creator', on_delete=models.SET_NULL, verbose_name="Создатель")
    category = models.ForeignKey(PostCategory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Тематика")
    list = models.ManyToManyField(PostList, related_name='post_list')

    created = models.DateTimeField(default=timezone.now, verbose_name="Создан")
    status = models.CharField(choices=STATUSES, default=STATUS_PROCESSING, max_length=5, verbose_name="Статус статьи")
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Текст")

    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    is_signature = models.BooleanField(default=True, verbose_name="Подпись автора")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    is_deleted = models.BooleanField(verbose_name="Удален", default=False)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.creator.get_full_name()

    @classmethod
    def create_post(cls, creator, text, category, lists, attach, community, parent, comments_enabled, is_signature, votes_on, status):
        from common.processing.post import get_post_processing

        # если списки для новой записи не выбраны, то мы вернём ошибку
        if not lists:
            raise ValidationError("Не выбран список для новой записи")

        # записываем правильно в поле прикрепленнх объектов сведения о них, если они есть
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        post = cls.objects.create(creator=creator,text=text,category=category,community=community,parent=parent,comments_enabled=comments_enabled,is_signature=is_signature,votes_on=votes_on,status=status,attach=_attach,)

        # привязываем новую запись к выбранным спискам записей
        for list_id in lists:
            post_list = PostList.objects.get(pk=list_id)
            post_list.post_list.add(post)

        # программа для проверки содержимого записи. Если все хорошо, то она меняет статус новой записи на STATUS_PUBLISHED
        get_post_processing(post)

        # если запись не в приватном списке, то создаём уведомления
        if not post.is_have_private_lists():
            from notify.models import Notify, Wall
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer

            channel_layer = get_channel_layer()

            # здесь мы создадим одну запись в модель Wall для новостей. А также по одной записи на каждого подписанта.
            # То есть персоналу сообщеста и всем подписанным на уведомления сообщества (CommunityProfileNotify) -
            # если запись имеет сообщество, и всем подписантам на уведомления пользователя (UserProfileNotify) -
            # если сообщество создается в ленту пользователя.
            if community:
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, attach="pos"+str(post.pk), verb="ITE")
                for user_id in community.get_memeber_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, community_id=community.pk, attach="pos"+str(post.pk), verb="ITE")
                    payload = {
                        'type': 'receive',
                        'key': 'notification',
                        'id': str(post.pk),
                        'community_id': str(community.pk),
                        'recipient_id': str(user_id),
                        'name': "c_post_create",
                    }
            else:
                Wall.objects.create(creator_id=creator.pk, attach="pos"+str(post.pk), verb="ITE")
                for user_id in creator.get_memeber_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, attach="pos"+str(post.pk), verb="ITE")
                payload = {
                    'type': 'receive',
                    'key': 'notification',
                    'id': str(post.pk),
                    'recipient_id': str(user_id),
                    'name': "u_post_create",
                }
            async_to_sync(channel_layer.group_send)('notification', payload)
        return post

    @classmethod
    def create_parent_post(cls, creator, community, attach):
        post = cls.objects.create(creator=creator, community=community, attach=attach, )
        return post

    def delete_post(self):
        try:
            from notify.models import Notify
            Notify.objects.filter(attach="goo" + str(self.pk)).update(status="C")
        except:
            pass
        self.is_deleted = True
        return self.save(update_fields=['is_deleted'])

    def abort_delete_post(self):
        try:
            from notify.models import Notify
            Notify.objects.filter(attach="pos" + str(self.pk)).update(status="R")
        except:
            pass
        self.is_deleted = False
        return self.save(update_fields=['is_deleted'])

    def get_u_new_parent(self, user):
        from common.attach.post_attach import get_u_news_parent
        return get_u_news_parent(self.parent, user)

    def get_c_new_parent(self, user):
        from common.attach.post_attach import get_c_news_parent
        return get_c_news_parent(self.parent, user)

    def get_u_post_parent(self, user):
        from common.attach.post_attach import get_u_posts_parent
        return get_u_posts_parent(self.parent, user)

    def get_c_post_parent(self, user):
        from common.attach.post_attach import get_c_posts_parent
        return get_c_posts_parent(self.parent, user)

    def get_u_attach(self, user):
        from common.attach.post_attach import get_u_post_attach
        return get_u_post_attach(self, user)

    def get_c_attach(self, user):
        from common.attach.post_attach import get_c_post_attach
        return get_c_post_attach(self, user)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def count_comments(self):
        parents = PostComment.objects.filter(post_id=self.pk, is_deleted=False)
        parents_count = parents.count()
        i = 0
        for comment in parents:
            i = i + comment.count_replies()
        i = i + parents_count
        if i == 0:
            return ''
        else:
            return i

    def __str__(self):
        return self.creator.get_full_name()

    def get_comments(self):
        comments_query = Q(post_id=self.pk)
        comments_query.add(Q(parent__isnull=True), Q.AND)
        return PostComment.objects.filter(comments_query)

    def is_fixed_in_community(self):
        try:
            list = PostList.objects.get(community_id=self.community.pk, type=PostList.FIX)
            if list.is_post_in_list(self.pk):
                return True
        except:
            pass
    def is_fixed_in_user(self):
        try:
            list = PostList.objects.get(creator_id=self.creator.pk, community__isnull=True, type=PostList.FIX)
            if list.is_post_in_list(self.pk):
                return True
        except:
            pass

    def is_can_fixed_in_community(self):
        """ мы уже проверили, есть ли пост в списке закрепов is_fixed_in_community. Потому осталось проверить, не полон ли список"""
        try:
            list = PostList.objects.get(community_id=self.community.pk, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=self.creator.pk, community_id=self.community.pk, type=PostList.FIX, name="Закрепленный список")
        if list.is_full_list():
            return ValidationError("Запись нельзя прикрепить.")
        else:
            return True
    def is_can_fixed_in_user(self):
        """ мы уже проверили, есть ли пост в списке закрепов is_fixed_in_user. Потому осталось проверить, не полон ли список"""
        try:
            list = PostList.objects.get(creator_id=self.creator.pk, community__isnull=True, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=self.creator.pk, type=PostList.FIX, name="Закрепленный список")
        if list.is_full_list():
            return ValidationError("Запись нельзя прикрепить.")
        else:
            return True

    def fixed_user_post(self, user_id):
        try:
            list = PostList.objects.get(creator_id=user_id, community__isnull=True, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=user_id, type=PostList.FIX, name="Закрепленный список")
        if not list.is_full_list():
            self.list.add(list)
            return True
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_user_post(self, user_id):
        try:
            list = PostList.objects.get(creator_id=user_id, community__isnull=True, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=user_id, type=PostList.FIX, name="Закрепленный список")
        if list.is_post_in_list(self.pk):
            self.list.remove(list)
            return True
        else:
            return ValidationError("Запись и так не в списке.")

    def fixed_community_post(self, community_id):
        try:
            list = PostList.objects.get(community_id=community_id, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=self.creator.pk, community_id=community_id, type=PostList.FIX, name="Закрепленный список")
        if not list.is_full_list():
            self.list.add(list)
            return True
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_community_post(self, community_id):
        try:
            list = PostList.objects.get(community_id=community_id, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=self.creator.pk, community_id=community_id, type=PostList.FIX, name="Закрепленный список")
        if list.is_post_in_list(self.pk):
            self.list.remove(list)
            return True
        else:
            return ValidationError("Запись и так не в списке.")

    def likes(self):
        from common.model.votes import PostVotes
        likes = PostVotes.objects.filter(parent_id=self.pk, vote__gt=0)
        return likes

    def dislikes(self):
        from common.model.votes import PostVotes
        dislikes = PostVotes.objects.filter(parent_id=self.pk, vote__lt=0)
        return dislikes

    def likes_count(self):
        from common.model.votes import PostVotes
        likes = PostVotes.objects.filter(parent_id=self.pk, vote__gt=0).values('pk').count()
        if likes > 0:
            return likes
        else:
            return ''
    def dislikes_count(self):
        from common.model.votes import PostVotes
        dislikes = PostVotes.objects.filter(parent_id=self.pk, vote__lt=0).values('pk').count()
        if dislikes > 0:
            return dislikes
        else:
            return ''

    def likes_count_ru(self):
        count = self.likes_count()
        if not count:
            return '<span data-count="like">' + str(0) + '</span> просмотров'
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            i = " просмотр"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            i = " просмотра"
        else:
            i = " просмотров"
        return '<span data-count="like">' + str(count) + '</span>' + i
    def dislikes_count_ru(self):
        count = self.dislikes_count()
        if not count:
            return '<span data-count="dislike">' + str(0) + '</span> просмотров'
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            i = " просмотр"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            i = " просмотра"
        else:
            i = " просмотров"
        return '<span data-count="dislike">' + str(count) + '</span>' + i

    def window_likes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__gt=0)[0:6]
    def is_have_likes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__gt=0).exists()
    def window_dislikes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__lt=0)[0:6]
    def is_have_dislikes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__lt=0).exists()

    def get_reposts(self):
        parents = Post.objects.filter(parent=self)
        return parents

    def get_window_reposts(self):
        parents = Post.objects.filter(parent=self)
        return parents[0:6]

    def count_reposts(self):
        parents = self.get_reposts()
        count_reposts = parents.values('pk').count()
        if count_reposts == 0:
            return ''
        else:
            return count_reposts

    def get_visiter_sity(self):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import UserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        sities = UserLocation.objects.filter(user_id__in=ids).distinct('city_ru')
        return sities

    def get_sity_count(self, sity):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import UserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        count = UserLocation.objects.filter(user_id__in=ids, city_ru=sity).values('pk').count()
        return count

    def all_visits_count(self):
        return self.post_visits_count()

    def get_list_pk(self):
        return self.list.all()[0].pk

    def get_lists(self):
        return self.list.all()

    def is_have_private_lists(self):
        for list in self.list.all():
            if list.is_private_list():
                return True
        return False

    def post_visits_count(self):
        from stst.models import PostNumbers
        return PostNumbers.objects.filter(post=self.pk).values('pk').count()

    def get_attach_photos(self):
        if "pho" in self.attach:
            query = []
            from gallery.models import Photo

            for item in self.attach.split(","):
                if item[:3] == "pho":
                    query.append(item[3:])
        return Photo.objects.filter(id__in=query)

    def get_attach_videos(self):
        if "pho" in self.attach:
            query = []
            from video.models import Video

            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)


class PostComment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "комментарий к записи"
        verbose_name_plural = "комментарии к записи"

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        get_comments = PostComment.objects.filter(parent=self).all()
        return get_comments

    def count_replies(self):
        return self.replies.filter(is_deleted=False).values("pk").count()

    def likes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__gt=0)

    def dislikes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__lt=0)

    def likes_count(self):
        from common.model.votes import PostCommentVotes
        qs = PostCommentVotes.objects.filter(item=self, vote__gt=0).values("pk").count()
        if qs > 0:
            return qs
        else:
            return ''

    def dislikes_count(self):
        from common.model.votes import PostCommentVotes
        qs = PostCommentVotes.objects.filter(item=self, vote__lt=0).values("pk").count()
        if qs > 0:
            return qs
        else:
            return ''

    def window_likes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__gt=0)[0:6]

    def window_dislikes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__lt=0)[0:6]

    def __str__(self):
        return self.commenter.get_full_name()

    @classmethod
    def create_comment(cls, commenter, attach, post, parent, text):
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        comment = PostComment.objects.create(commenter=commenter, attach=_attach, parent=parent, post=post, text=text, created=timezone.now())
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "comment_item",
            "actor_name": comment.commenter.get_full_name()
        }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        return comment

    def count_replies_ru(self):
        count = self.replies.filter(is_deleted=False).values("pk").count()
        a, b= count % 10, count % 100
        if (a == 1) and (b != 11):
            return ''.join([str(count), " ответ"])
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return ''.join([str(count), " ответа"])
        else:
            return ''.join([str(count), " ответов"])

    def get_u_attach(self, user):
        from common.attach.comment_attach import get_u_comment_attach
        return get_u_comment_attach(self, user)

    def get_c_attach(self, user):
        from common.attach.comment_attach import get_c_comment_attach
        return get_c_comment_attach(self, user)

    def get_attach_photos(self):
        if "pho" in self.attach:
            query = []
            from gallery.models import Photo

            for item in self.attach.split(","):
                if item[:3] == "pho":
                    query.append(item[3:])
        return Photo.objects.filter(id__in=query)

    def get_attach_videos(self):
        if "pho" in self.attach:
            query = []
            from video.models import Video

            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)

    def delete_comment(self):
        try:
            from notify.models import Notify
            if self.parent:
                Notify.objects.filter(attach="por" + str(self.pk)).update(status="C")
            else:
                Notify.objects.filter(attach="poc" + str(self.pk)).update(status="C")
        except:
            pass
        self.is_deleted = True
        return self.save(update_fields=['is_deleted'])

    def abort_delete_comment(self):
        try:
            from notify.models import Notify
            if self.parent:
                Notify.objects.filter(attach="por" + str(self.pk)).update(status="R")
            else:
                Notify.objects.filter(attach="poc" + str(self.pk)).update(status="R")
        except:
            pass
        self.is_deleted = False
        return self.save(update_fields=['is_deleted'])
