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
    MAIN, LIST, MANAGER, THIS_PROCESSING, PRIVATE, THIS_FIXED, THIS_DRAFT = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI', '_FIX', '_DRA'
    THIS_DELETED, THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    THIS_CLOSED, THIS_CLOSED_PRIVATE, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER, THIS_CLOSED_FIXED = '_CLO', '_CLOP', '_CLOM', '_CLOMA', '_CLOF'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(THIS_PROCESSING, 'Обработка'),(THIS_FIXED, 'Закреплённый'),(THIS_DRAFT, 'Предложка'),
        (THIS_DELETED, 'Удалённый'),(THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),
        (THIS_CLOSED, 'Закрытый менеджером'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MAIN, 'Закрытый основной'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),(THIS_CLOSED_FIXED, 'Закрытый закреплённый'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_postlist', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_postlist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=THIS_PROCESSING, verbose_name="Тип списка")
    order = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    def __str__(self):
        return self.name + " - " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список записей"
        verbose_name_plural = "списки записей"
        ordering = ['order']

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            PostList.objects.create(community=instance, type=PostList.MAIN, name="Основной список", creator=instance.creator)
            PostList.objects.create(community=instance, type=PostList.THIS_FIXED, name="Закреплённый список", creator=instance.creator)
            PostList.objects.create(community=instance, type=PostList.THIS_DRAFT, name="Предложка", creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            PostList.objects.create(creator=instance, type=PostList.MAIN, name="Основной список")
            PostList.objects.create(creator=instance, type=PostList.THIS_FIXED, name="Закреплённый список")
            PostList.objects.create(creator=instance, type=PostList.THIS_DRAFT, name="Предложка")

    def is_item_in_list(self, item_id):
        return self.post_list.filter(pk=item_id).values("pk").exists()

    def get_staff_items(self):
        query = Q(status="PUB")|Q(status="PRI")
        return self.post_list.select_related('creator').only('creator__id', 'created').filter(query, list=self)
    def get_items(self):
        return self.post_list.filter(list=self,status="PUB")
    def get_fix_items(self):
        return self.post_list.select_related('creator').only('creator__id', 'created').filter(list=self,status="_FIX")
    def get_manager_items(self):
        return self.post_list.filter(status="MAN")
    def count_items(self):
        return self.post_list.filter(Q(status="PUB")|Q(status="PRI")).values("pk").count()
    def count_fix_items(self):
        return self.post_list.filter(status="_FIX").values("pk").count()

    def is_not_empty(self):
        return self.post_list.filter(Q(status="PUB")|Q(status="PRI")).values("pk").exists()

    def get_posts_ids(self):
        ids = self.post_list.filter(status="_FIX").values("pk")
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
        return self.type == self.THIS_FIXED
    def is_list(self):
        return self.type == self.LIST
    def is_deleted(self):
        return self.type == self.THIS_DELETED
    def is_closed(self):
        return self.type == self.THIS_CLOSED
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type[0] == "_"

    @classmethod
    def get_user_staff_lists(cls, user_pk):
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
        query.add(Q(Q(type="LIS")|Q(type="MAI")), Q.AND)
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
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
        query.add(Q(Q(type="LIS")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing.post import get_post_list_processing
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="POL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_post_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="POL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_post_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="POL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_post_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="POL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_post_list_notify")
        get_post_list_processing(list, PostList.LIST)
        return list
    def edit_list(self, name, description, order, is_public):
        from common.processing.post import get_post_list_processing
        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
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

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = PostList.THIS_DELETED
        elif self.type == "PRI":
            self.type = PostList.THIS_DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = PostList.THIS_DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_list(self):
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
            self.type = PostList.THIS_CLOSED
        elif self.type == "MAI":
            self.type = PostList.THIS_CLOSED_MAIN
        elif self.type == "PRI":
            self.type = PostList.THIS_CLOSED_PRIVATE
        elif self.type == "FIX":
            self.type = PostList.THIS_CLOSED_FIXED
        elif self.type == "MAN":
            self.type = PostList.THIS_CLOSED_MANAGER
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
            self.type = PostList.THIS_FIXED
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
    THIS_PROCESSING, THIS_DRAFT, THIS_FIXED, PUBLISHED, PRIVATE, MANAGER, THIS_DELETED, THIS_CLOSED, THIS_MESSAGE = 'PRO',"_DRA","_FIX", 'PUB','PRI','MAN','_DEL','_CLO', '_MES'
    THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER, THIS_CLOSED_PRIVATE, THIS_CLOSED_MANAGER = '_DELP','_DELM','_CLOP','_CLOM'
    STATUS = (
        (THIS_PROCESSING, 'Обработка'),(THIS_DRAFT, 'Черновик'),(THIS_FIXED, 'Закреплен'), (PUBLISHED, 'Опубликовано'),(THIS_DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(THIS_CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),(THIS_MESSAGE, 'Репост в сообщения'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")

    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="thread")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='post_creator', on_delete=models.SET_NULL, verbose_name="Создатель")
    category = models.ForeignKey(PostCategory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Тематика")
    list = models.ManyToManyField(PostList, related_name='post_list')

    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    status = models.CharField(choices=STATUS, default=THIS_PROCESSING, max_length=5, verbose_name="Статус статьи")
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

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-created"]

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
    def create_post(cls, creator, text, category, lists, attach, parent, comments_enabled, is_signature, votes_on, is_public, community):
        from common.processing.post import get_post_processing
        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для новой записи")
        private = 0
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        post = cls.objects.create(creator=creator,text=text,category=category,parent=parent,community=community,comments_enabled=comments_enabled,is_signature=is_signature,votes_on=votes_on,attach=_attach,)
        if community:
            community.plus_posts(1)
        else:
            creator.plus_posts(1)

        for list_id in lists:
            post_list = PostList.objects.get(pk=list_id)
            if post_list.is_private():
                private = 1
            post_list.post_list.add(post)

        if not private and is_public:
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
        return post

    def edit_post(self, text, category, lists, attach, parent, comments_enabled, is_signature, votes_on, is_public):
        from common.processing.post  import get_post_processing

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

        self.text = text
        self.category = category
        self.lists = lists
        self.attach = _attach
        self.comments_enabled = comments_enabled
        self.is_signature = is_signature
        self.votes_on = votes_on

        if is_public and self.is_private():
            get_post_processing(self, Post.PUBLISHED)
            self.make_publish()
        elif not is_public and self.is_open():
            get_post_processing(self, Post.PRIVATE)
            self.make_private()
        else:
            get_post_processing(self, self.status)
        return self.save()

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Post.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Post.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")

    def delete_post(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Post.THIS_DELETED
        elif self.status == "PRI":
            self.status = Post.THIS_DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Post.THIS_DELETED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_posts(1)
        else:
            self.creator.minus_posts(1)
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def restore_post(self, community):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = Post.PUBLISHED
        elif self.status == "_DELP":
            self.status = Post.PRIVATE
        elif self.status == "_DELM":
            self.status = Post.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_posts(1)
        else:
            self.creator.plus_posts(1)
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, comunity):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Post.THIS_CLOSED
        elif self.status == "PRI":
            self.status = Post.THIS_CLOSED_PRIVATE
        elif self.status == "MAN":
            self.status = Post.THIS_CLOSED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_posts(1)
        else:
            self.creator.minus_posts(1)
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.status == "_CLO":
            self.status = Post.PUBLISHED
        elif self.status == "_CLOP":
            self.status = Post.PRIVATE
        elif self.status == "_CLOM":
            self.status = Post.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_posts(1)
        else:
            self.creator.plus_posts(1)
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
        from common.attach.post_attach import get_u_post_attach
        return get_u_post_attach(self, user)

    def get_c_attach(self, user):
        from common.attach.post_attach import get_c_post_attach
        return get_c_post_attach(self, user)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def count_comments(self):
        if self.comment == 0:
            return ''
        else:
            return self.comment

    def get_comments(self):
        return PostComment.objects.filter(post_id=self.pk, parent__isnull=True, status="PUB")

    def is_fixed_in_community(self):
        list = PostList.objects.get(community_id=self.community.pk, type=PostList.THIS_FIXED)
        return list.is_item_in_list(self.pk)
    def is_fixed_in_user(self):
        list = PostList.objects.get(creator_id=self.creator.pk, community__isnull=True, type=PostList.THIS_FIXED)
        return list.is_item_in_list(self.pk)

    def is_can_fixed_in_community(self):
        """ мы уже проверили, есть ли пост в списке закрепов is_fixed_in_community. Потому осталось проверить, не полон ли список"""
        return self.is_full_list()
    def is_can_fixed_in_user(self):
        """ мы уже проверили, есть ли пост в списке закрепов is_fixed_in_user. Потому осталось проверить, не полон ли список"""
        return self.is_full_list()

    def fixed_user_post(self, user_id):
        list = PostList.objects.get(creator_id=user_id, community__isnull=True, type=PostList.THIS_FIXED)
        if not list.is_full_list():
            self.list.add(list)
            self.status = Post.THIS_FIXED
            return self.save(update_fields=["status"])
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_user_post(self, user_id):
        list = PostList.objects.get(creator_id=user_id, community__isnull=True, type=PostList.THIS_FIXED)
        if list.is_item_in_list(self.pk):
            self.list.remove(list)
            self.status = Post.PUBLISHED
            return self.save(update_fields=["status"])
        else:
            return ValidationError("Запись и так не в списке.")

    def fixed_community_post(self, community_id):
        list = PostList.objects.get(community_id=community_id, type=PostList.THIS_FIXED)
        if not list.is_full_list():
            self.list.add(list)
            self.status = Post.THIS_FIXED
            return self.save(update_fields=["status"])
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_community_post(self, community_id):
        list = PostList.objects.get(community_id=community_id, type=PostList.THIS_FIXED)
        if list.is_item_in_list(self.pk):
            self.list.remove(list)
            self.status = Post.PUBLISHED
            return self.save(update_fields=["status"])
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
        return self.list.all()[0].pk

    def get_lists(self):
        return self.list.all()

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
        if "pho" in self.attach:
            query = []
            from video.models import Video

            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)


class PostComment(models.Model):
    EDITED, PUBLISHED, THIS_PROCESSING = 'EDI', 'PUB', '_PRO'
    THIS_DELETED, THIS_EDITED_DELETED = '_DEL', '_DELE'
    THIS_CLOSED, THIS_EDITED_CLOSED = '_CLO', '_CLOE'
    STATUS = (
        (PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Удалённый'), (THIS_EDITED_DELETED, 'Удалённый изменённый'),
        (THIS_CLOSED, 'Закрытый менеджером'), (THIS_EDITED_CLOSED, 'Закрытый изменённый'),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    status = models.CharField(max_length=5, choices=STATUS, default=THIS_PROCESSING, verbose_name="Тип альбома")

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
        return self.replies.filter(~Q(status__contains="_")).only("pk")

    def count_replies(self):
        return self.replies.filter(Q(status=PostComment.EDITED)|Q(status=PostComment.PUBLISHED)).values("pk").count()

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

    def delete_comment(self):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = PostComment.THIS_DELETED
        elif self.status == "EDI":
            self.status = PostComment.THIS_EDITED_DELETED
        self.save(update_fields=['status'])
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
    def restore_comment(self):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = PostComment.PUBLISHED
        elif self.status == "_DELE":
            self.status = PostComment.EDITED
        self.save(update_fields=['status'])
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
        if self.status == "PUB":
            self.status = PostComment.THIS_CLOSED
        elif self.status == "EDI":
            self.status = PostComment.THIS_EDITED_CLOSED
        self.save(update_fields=['status'])
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
        if self.status == "_CLO":
            self.status = PostComment.PUBLISHED
        elif self.status == "_CLOE":
            self.status = PostComment.EDITED
        self.save(update_fields=['status'])
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
