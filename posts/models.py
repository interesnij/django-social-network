import uuid
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.postgres.indexes import BrinIndex
from common.utils import try_except
from django.db.models.signals import post_save
from django.dispatch import receiver
from communities.models import Community


class PostList(models.Model):
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE, FIXED, DRAFT = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI', '_FIX', '_DRA'
    DELETED, DELETED_PRIVATE, DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER, CLOSED_FIXED = '_CLO', '_CLOP', '_CLOM', '_CLOMA', '_CLOF'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),(FIXED, 'Закреплённый'),(DRAFT, 'Предложка'),
        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),(CLOSED_FIXED, 'Закрытый закреплённый'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_postlist', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_postlist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=PROCESSING, verbose_name="Тип списка")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + " - " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список записей"
        verbose_name_plural = "списки записей"

    def get_order(self):
        from users.model.list import UserPostListPosition
        return UserPostListPosition.objects.get(list=self.pk)

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            list_1 = PostList.objects.create(community=instance, type=PostList.MAIN, name="Основной список", creator=instance.creator)
            PostList.objects.create(community=instance, type=PostList.FIXED, name="Закреплённый список", creator=instance.creator)
            list_2 = PostList.objects.create(community=instance, type=PostList.DRAFT, name="Предложка", creator=instance.creator)
            from communities.model.list import CommunityPostListPosition
            CommunityPostListPosition.objects.create(community=instance.pk, list=list_1.pk, position=1)
            CommunityPostListPosition.objects.create(community=instance.pk, list=list_2.pk, position=2)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            list_1 = PostList.objects.create(creator=instance, type=PostList.MAIN, name="Основной список")
            PostList.objects.create(creator=instance, type=PostList.FIXED, name="Закреплённый список")
            list_2 = PostList.objects.create(creator=instance, type=PostList.DRAFT, name="Предложка")
            from users.model.list import UserPostListPosition
            UserPostListPosition.objects.create(user=instance.pk, list=list_1.pk, position=1)
            UserPostListPosition.objects.create(user=instance.pk, list=list_2.pk, position=2)

    def is_item_in_list(self, item_id):
        return self.post_list.filter(pk=item_id).values("pk").exists()

    def get_staff_items(self):
        query = Q(list=self)
        query.add(Q(Q(type="PUB")|Q(type="PRI")), Q.AND)
        return self.post_list.select_related('creator', 'community').only('creator__id', 'community__id', 'created').filter(query)
    def get_items(self):
        return self.post_list.select_related('creator').only('creator__id', 'created').filter(list=self,type="PUB")
    def get_fix_items(self):
        return self.post_list.select_related('creator').only('creator__id', 'created').filter(list=self,type="_FIX")
    def get_manager_items(self):
        return self.post_list.filter(type="MAN")
    def count_items(self):
        return self.post_list.filter(Q(type="PUB")|Q(type="PRI")).values("pk").count()
    def count_fix_items(self):
        return self.post_list.filter(type="_FIX").values("pk").count()

    def is_not_empty(self):
        return self.post_list.filter(Q(type="PUB")|Q(type="PRI")).values("pk").exists()

    def get_posts_ids(self):
        ids = self.post_list.filter(type="_FIX").values("pk")
        return [id['pk'] for id in ids]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids()

    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def is_community_can_add_list(self, community_id):
        return self.community.pk != community_id and community_id not in self.get_communities_ids()

    def is_community_can_delete_list(self, community_id):
        return self.community.pk != community_id and community_id in self.get_communities_ids()

    def get_users_ids(self):
        users = self.users.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in communities]

    def is_full_list(self):
        return self.is_fix_list() and self.count_items() > 10

    def is_main(self):
        return self.type == self.MAIN
    def is_fix_list(self):
        return self.type == self.FIXED
    def is_list(self):
        return self.type == self.LIST
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type[0] == "_"
    def is_have_edit(self):
        return self.is_list() or self.is_private()

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        from users.model.list import UserPostListPosition
        try:
            return cls.objects.filter(id__in=[i['list'] for i in UserPostListPosition.objects.filter(user=self.pk).values("list")])
        except:
            query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
            query.add(~Q(type__contains="_"), Q.AND)
            return cls.objects.filter(query)
    @classmethod
    def get_user_lists(cls, user_pk):
        query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
        query.add(Q(Q(type="LIS")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
        query.add(~Q(type__contains="_"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
        query.add(~Q(type__contains="_"), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_community_lists(cls, community_pk):
        query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
        query.add(Q(Q(type="LIS")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
        query.add(~Q(type__contains="_"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def create_list(cls, creator, name, description, community, is_public):
        from notify.models import Notify, Wall
        from common.processing.post import get_post_list_processing

        list = cls.objects.create(creator=creator,name=name,description=description, community=community)
        if community:
            from communities.model.list import CommunityPostListPosition
            CommunityPostListPosition.objects.create(community=community.pk, list=list.pk, position=PostList.get_community_lists_count(community.pk))
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="POL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_post_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="POL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_post_list_notify")
        else:
            from users.model.list import UserPostListPosition
            UserPostListPosition.objects.create(user=creator.pk, list=list.pk, position=PostList.get_user_lists_count(creator.pk))
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="POL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_post_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="POL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_post_list_notify")
        get_post_list_processing(list, PostList.LIST)
        return list

    def edit_list(self, name, description, is_public):
        from common.processing.post import get_post_list_processing

        self.name = name
        self.description = description
        self.save()
        if is_public:
            get_post_list_processing(self, PostList.LIST)
            self.make_publish()
        else:
            get_post_list_processing(self, PostList.PRIVATE)
            self.make_private()
        return self

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = PostList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = PostList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = PostList.DELETED
        elif self.type == "PRI":
            self.type = PostList.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = PostList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = PostList.LIST
        elif self.type == "_DELP":
            self.type = PostList.PRIVATE
        elif self.type == "_DELM":
            self.type = PostList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = PostList.CLOSED
        elif self.type == "MAI":
            self.type = PostList.CLOSED_MAIN
        elif self.type == "PRI":
            self.type = PostList.CLOSED_PRIVATE
        elif self.type == "FIX":
            self.type = PostList.CLOSED_FIXED
        elif self.type == "MAN":
            self.type = PostList.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = PostList.LIST
        elif self.type == "_CLOM":
            self.type = PostList.MAIN
        elif self.type == "_CLOP":
            self.type = PostList.PRIVATE
        elif self.type == "_CLOF":
            self.type = PostList.FIXED
        elif self.type == "_CLOM":
            self.type = PostList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")


class PostCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Тематика")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Тематика постов"
		verbose_name_plural = "Тематики постов"


class Post(models.Model):
    PROCESSING, DRAFT, FIXED, PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED, MESSAGE = 'PRO',"_DRA","_FIX", 'PUB','PRI','MAN','_DEL','_CLO', '_MES'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = '_DELP','_DELM','_CLOP','_CLOM'
    TYPE = (
        (PROCESSING, 'Обработка'),(DRAFT, 'Черновик'),(FIXED, 'Закреплен'), (PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),(MESSAGE, 'Репост в сообщения'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")

    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="thread")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='post_creator', on_delete=models.SET_NULL, verbose_name="Создатель")
    category = models.ForeignKey(PostCategory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Тематика")
    list = models.ForeignKey(PostList, blank=True, null=True, on_delete=models.SET_NULL, related_name='post_list')

    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    type = models.CharField(choices=TYPE, default=PROCESSING, max_length=5, verbose_name="Статус статьи")
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Текст")

    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    is_signature = models.BooleanField(default=True, verbose_name="Подпись автора")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    community = models.ForeignKey('communities.Community', related_name='post_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    ad_view = models.PositiveIntegerField(default=0, verbose_name="Кол-во рекламных просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-order"]

    def __str__(self):
        return self.creator.get_full_name()

    def plus_likes(self, count):
        self.like += count
        return self.save(update_fields=['like'])
    def minus_likes(self, count):
        self.like -= count
        return self.save(update_fields=['like'])
    def plus_dislikes(self, count):
        self.dislike += count
        return self.save(update_fields=['dislike'])
    def minus_dislikes(self, count):
        self.dislike -= count
        return self.save(update_fields=['dislike'])
    def plus_comments(self, count):
        self.comment += count
        return self.save(update_fields=['comment'])
    def minus_comments(self, count):
        self.comment -= count
        return self.save(update_fields=['comment'])
    def plus_views(self, count):
        self.view += count
        return self.save(update_fields=['view'])
    def plus_ad_views(self, count):
        self.ad_view += count
        return self.save(update_fields=['ad_view'])
    def plus_reposts(self, count):
        self.repost += count
        return self.save(update_fields=['repost'])
    def minus_reposts(self, count):
        self.repost -= count
        return self.save(update_fields=['repost'])

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"

    def send_like(self, user, community):
        import json
        from common.model.votes import PostVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        if not self.votes_on:
            from django.http import Http404
            raise Http404
        try:
            item = PostVotes.objects.get(parent=self, user=user)
            if item.vote != PostVotes.LIKE:
                item.vote = PostVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except PostVotes.DoesNotExist:
            PostVotes.objects.create(parent=self, user=user, vote=PostVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, self.pk, "POS", "u_post_notify", "LIK")
                community_wall(user, community, None, self.pk, "POS", "u_post_notify", "LIK")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, self.pk, "POS", "u_post_notify", "LIK")
                user_wall(user, None, self.pk, "POS", "u_post_notify", "LIK")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import PostVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        if not self.votes_on:
            from django.http import Http404
            raise Http404
        try:
            item = PostVotes.objects.get(parent=self, user=user)
            if item.vote != PostVotes.DISLIKE:
                item.vote = PostVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except PostVotes.DoesNotExist:
            PostVotes.objects.create(parent=self, user=user, vote=PostVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, self.pk, "POS", "u_post_notify", "DIS")
                community_wall(user, community, None, self.pk, "POS", "u_post_notify", "DIS")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, self.pk, "POS", "u_post_notify", "DIS")
                user_wall(user, None, self.pk, "POS", "u_post_notify", "DIS")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

    @classmethod
    def create_post(cls, creator, text, category, list, attach, parent, comments_enabled, is_signature, votes_on, is_public, community):
        from common.processing.post import get_post_processing
        #if not text or not attach:
        #    from rest_framework.exceptions import ValidationError
        #    raise ValidationError("Нет текста и вложений")
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        _list = PostList.objects.get(pk=list)

        _list.count += 1
        _list.save(update_fields=["count"])
        post = cls.objects.create(creator=creator,list=_list,order=_list.count,text=text,category=category,parent=parent,community=community,comments_enabled=comments_enabled,is_signature=is_signature,votes_on=votes_on,attach=_attach,)

        if not _list.is_private() and is_public:
            get_post_processing(post, Post.PUBLISHED)
            if community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="POS", object_id=post.pk, verb="ITE")
                community_send_wall(post.pk, creator.pk, community.pk, None, "create_c_post_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="POS", object_id=post.pk, verb="ITE")
                    community_send_notify(post.pk, creator.pk, user_id, community.pk, None, "create_c_post_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall
                Wall.objects.create(creator_id=creator.pk, type="POS", object_id=post.pk, verb="ITE")
                user_send_wall(post.pk, None, "create_u_post_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="POS", object_id=post.pk, verb="ITE")
                    user_send_notify(post.pk, creator.pk, user_id, None, "create_u_post_notify")
        else:
            get_post_processing(post, Post.PRIVATE)
        if community:
            community.plus_posts(1)
        else:
            creator.plus_posts(1)
        return post

    def edit_post(self, text, list, category, attach, parent, comments_enabled, is_signature, votes_on, is_public):
        from common.processing.post  import get_post_processing

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        _list = PostList.objects.get(pk=list)
        if self.list.pk != list:
            self.list.count -= 1
            self.list.save(update_fields=["count"])
            _list.count += 1
            _list.save(update_fields=["count"])

        self.text = text
        self.category = category
        self.attach = _attach
        self.comments_enabled = comments_enabled
        self.is_signature = is_signature
        self.list = _list
        self.votes_on = votes_on

        if is_public and self.is_private():
            get_post_processing(self, Post.PUBLISHED)
            self.make_publish()
        elif not is_public and self.is_open():
            get_post_processing(self, Post.PRIVATE)
            self.make_private()
        else:
            get_post_processing(self, self.type)
        return self.save()

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Post.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Post.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Post.DELETED
        elif self.type == "PRI":
            self.type = Post.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = Post.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_posts(1)
        else:
            self.creator.minus_posts(1)
        self.list.count -= 1
        list.save(update_fields=["count"])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Post.PUBLISHED
        elif self.type == "_DELP":
            self.type = Post.PRIVATE
        elif self.type == "_DELM":
            self.type = Post.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_posts(1)
        else:
            self.creator.plus_posts(1)
        self.list.count += 1
        list.save(update_fields=["count"])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, comunity):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Post.CLOSED
        elif self.type == "PRI":
            self.type = Post.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = Post.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_posts(1)
        else:
            self.creator.minus_posts(1)
        self.list.count -= 1
        list.save(update_fields=["count"])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Post.PUBLISHED
        elif self.type == "_CLOP":
            self.type = Post.PRIVATE
        elif self.type == "_CLOM":
            self.type = Post.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_posts(1)
        else:
            self.creator.plus_posts(1)
        self.list.count += 1
        list.save(update_fields=["count"])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")

    @classmethod
    def create_parent_post(cls, creator, community, attach):
        post = cls.objects.create(creator=creator, community=community, attach=attach, )
        return post

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
        from common.attach.post_elements import get_post_attach
        return get_post_attach(self, user)

    def get_c_attach(self, user):
        from common.attach.post_elements import get_post_attach
        return get_post_attach(self, user)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def count_comments(self):
        if self.comment == 0:
            return ''
        else:
            return self.comment

    def get_comments(self):
        return PostComment.objects.filter(post_id=self.pk, parent__isnull=True, type="PUB")

    def is_fixed_in_community(self):
        list = PostList.objects.get(community_id=self.community.pk, type=PostList.FIXED)
        return list.is_item_in_list(self.pk)
    def is_fixed_in_user(self):
        list = PostList.objects.get(creator_id=self.creator.pk, community__isnull=True, type=PostList.FIXED)
        return list.is_item_in_list(self.pk)

    def is_can_fixed_in_community(self):
        """ мы уже проверили, есть ли пост в списке закрепов is_fixed_in_community. Потому осталось проверить, не полон ли список"""
        return self.is_full_list()
    def is_can_fixed_in_user(self):
        """ мы уже проверили, есть ли пост в списке закрепов is_fixed_in_user. Потому осталось проверить, не полон ли список"""
        return self.is_full_list()

    def fixed_user_post(self, user_id):
        list = PostList.objects.get(creator_id=user_id, community__isnull=True, type=PostList.FIXED)
        if not list.is_full_list():
            self.list.add(list)
            self.type = Post.FIXED
            return self.save(update_fields=["type"])
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_user_post(self, user_id):
        list = PostList.objects.get(creator_id=user_id, community__isnull=True, type=PostList.FIXED)
        if list.is_item_in_list(self.pk):
            self.list.remove(list)
            self.type = Post.PUBLISHED
            return self.save(update_fields=["type"])
        else:
            return ValidationError("Запись и так не в списке.")

    def fixed_community_post(self, community_id):
        list = PostList.objects.get(community_id=community_id, type=PostList.FIXED)
        if not list.is_full_list():
            self.list.add(list)
            self.type = Post.FIXED
            return self.save(update_fields=["type"])
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_community_post(self, community_id):
        list = PostList.objects.get(community_id=community_id, type=PostList.FIXED)
        if list.is_item_in_list(self.pk):
            self.list.remove(list)
            self.type = Post.PUBLISHED
            return self.save(update_fields=["type"])
        else:
            return ValidationError("Запись и так не в списке.")

    def likes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__gt=0)

    def dislikes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__lt=0)

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''
    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
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
        return self.like > 0
    def window_dislikes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__lt=0)[0:6]
    def is_have_dislikes(self):
        return self.dislike > 0

    def get_reposts(self):
        return Post.objects.filter(parent=self)

    def get_window_reposts(self):
        return Post.objects.filter(parent=self)[0:6]

    def count_reposts(self):
        if self.repost == 0:
            return ''
        else:
            return self.repost

    def get_visiter_sity(self):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import UserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        return UserLocation.objects.filter(user_id__in=ids).distinct('city_ru')

    def get_sity_count(self, sity):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import UserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        return UserLocation.objects.filter(user_id__in=ids, city_ru=sity).values('pk').count()

    def all_visits_count(self):
        count = self.visits_count() + self.ad_visits_count()
        if count == 0:
            return ''
        else:
            return count

    def get_list_pk(self):
        return self.list.pk

    def is_have_private_lists(self):
        for list in self.list.all():
            if list.is_private_list():
                return True
        return False

    def visits_count(self):
        return self.view
    def ad_visits_count(self):
        return self.ad_view

    def get_attach_photos(self):
        if "pho" in self.attach:
            query = []
            from gallery.models import Photo

            for item in self.attach.split(","):
                if item[:3] == "pho":
                    query.append(item[3:])
        return Photo.objects.filter(id__in=query)

    def get_attach_videos(self):
        if "vid" in self.attach:
            query = []
            from video.models import Video

            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)
    def is_private(self):
        return self.type == self.PRIVATE


class PostComment(models.Model):
    EDITED, PUBLISHED, PROCESSING = 'EDI', 'PUB', '_PRO'
    DELETED, EDITED_DELETED = '_DEL', '_DELE'
    CLOSED, EDITED_CLOSED = '_CLO', '_CLOE'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(PROCESSING, 'Обработка'),
        (DELETED, 'Удалённый'), (EDITED_DELETED, 'Удалённый изменённый'),
        (CLOSED, 'Закрытый менеджером'), (EDITED_CLOSED, 'Закрытый изменённый'),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    type = models.CharField(max_length=5, choices=TYPE, default=PROCESSING, verbose_name="Тип альбома")

    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "комментарий к записи"
        verbose_name_plural = "комментарии к записи"

    def __str__(self):
        return self.commenter.get_full_name()

    def send_like(self, user, community):
        import json
        from common.model.votes import PostCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = PostCommentVotes.objects.get(item=self, user=user)
            if item.vote != PostCommentVotes.LIKE:
                item.vote = PostCommentVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except PostCommentVotes.DoesNotExist:
            PostCommentVotes.objects.create(item=self, user=user, vote=PostCommentVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_post_comment_notify", "LRE")
                    community_wall(user, community, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "POSC", "u_post_notify", "LRE")
                    user_wall(user, None, self.pk, "POSC", "u_post_notify", "LCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
                    community_wall(user, community, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
                    user_wall(user, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import PostCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = PostCommentVotes.objects.get(item=self, user=user)
            if item.vote != PostCommentVotes.DISLIKE:
                item.vote = PostCommentVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except PostCommentVotes.DoesNotExist:
            PostCommentVotes.objects.create(item=self, user=user, vote=PostCommentVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_post_comment_notify", "DRE")
                    community_wall(user, community, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "POSC", "u_post_comment_notify", "DRE")
                    user_wall(user, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
                    community_wall(user, community, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
                    user_wall(user, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        return self.replies.filter(~Q(type__contains="_")).only("pk")

    def count_replies(self):
        return self.replies.filter(Q(type=PostComment.EDITED)|Q(type=PostComment.PUBLISHED)).values("pk").count()

    def likes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__gt=0)

    def dislikes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__lt=0)

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''

    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
        else:
            return ''

    def reposts_count(self):
        if self.repost > 0:
            return self.repost
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
    def create_comment(cls, commenter, attach, post, parent, text, community):
        from common.processing.post import get_post_comment_processing
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        comment = PostComment.objects.create(commenter=commenter, attach=_attach, parent=parent, post=post, text=text)
        post.comment += 1
        post.save(update_fields=["comment"])
        if parent:
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(comment.commenter, community, None, comment.pk, "POSC", "u_post_comment_notify", "REP")
                community_wall(comment.commenter, community, None, comment.pk, "POSC", "u_post_comment_notify", "REP")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(comment.commenter, None, comment.pk, "POSC", "u_post_comment_notify", "REP")
                user_wall(comment.commenter, None, comment.pk, "POSC", "u_post_comment_notify", "REP")
        else:
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(comment.commenter, community, None, comment.pk, "POSC", "u_post_comment_notify", "COM")
                community_wall(comment.commenter, community, None, comment.pk, "POSC", "u_post_comment_notify", "COM")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(comment.commenter, None, comment.pk, "POSC", "u_post_comment_notify", "COM")
                user_wall(comment.commenter, None, comment.pk, "POSC", "u_post_comment_notify", "COM")
        get_post_comment_processing(comment)
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

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = PostComment.DELETED
        elif self.type == "EDI":
            self.type = PostComment.EDITED_DELETED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.post.comment -= 1
            self.parent.post.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.post.comment -= 1
            self.post.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = PostComment.PUBLISHED
        elif self.type == "_DELE":
            self.type = PostComment.EDITED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.post.comment += 1
            self.parent.post.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.post.comment += 1
            self.post.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = PostComment.CLOSED
        elif self.type == "EDI":
            self.type = PostComment.EDITED_CLOSED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.post.comment -= 1
            self.parent.post.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.post.comment -= 1
            self.post.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = PostComment.PUBLISHED
        elif self.type == "_CLOE":
            self.type = PostComment.EDITED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.post.comment += 1
            self.parent.post.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.post.comment += 1
            self.post.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").update(status="R")
