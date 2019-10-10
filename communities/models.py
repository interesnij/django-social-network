from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count
from pilkit.processors import ResizeToFill, ResizeToFit
from communities.helpers import upload_to_community_avatar_directory, upload_to_community_cover_directory
from posts.models import Post
from imagekit.models import ProcessedImageField
from users.models import User
from moderation.models import ModeratedObject, ModerationCategory


class CommunityCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Название")
    avatar = models.ImageField(blank=False, null=True, verbose_name="Аватар")
    order = models.IntegerField(default=0, verbose_name="Номер")

    def __str__(self):
        return 'Категория: ' + self.name


class CommunitySubCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Название")
    sudcategory = models.ForeignKey(CommunityCategory, on_delete=models.CASCADE, related_name='community_categories', verbose_name="Подкатегория сообщества")
    avatar = models.ImageField(blank=False, null=True, verbose_name="Аватар")
    order = models.IntegerField(default=0, verbose_name="Номер")

    def __str__(self):
        return 'ПодКатегория: ' + self.name


class Community(models.Model):
    moderated_object = GenericRelation(ModeratedObject, related_query_name='communities',verbose_name="Модерация")
    category = models.ForeignKey(CommunitySubCategory, on_delete=models.CASCADE, related_name='community_sub_categories', verbose_name="Подкатегория сообщества")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities', null=False, blank=False, verbose_name="Создатель")
    name = models.CharField(max_length=settings.COMMUNITY_CATEGORY_NAME_MAX_LENGTH, blank=False, null=False,
                            verbose_name="Имя")
    title = models.CharField(max_length=settings.COMMUNITY_CATEGORY_TITLE_MAX_LENGTH, blank=False, null=False, verbose_name="Заголовок" )
    description = models.CharField(max_length=300, blank=False,
                                   null=True, verbose_name="Описание" )
    rules = models.TextField(max_length=100, blank=False,
                             null=True, verbose_name="Правила")
    avatar = models.ImageField(blank=False, null=True, upload_to=upload_to_community_avatar_directory, verbose_name="Аватар")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    starrers = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='favorite_communities', verbose_name="Подписчики")
    banned_users = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='banned_of_communities', verbose_name="Черный список")
    status = models.CharField(max_length=100, blank=True, null=True, verbose_name="статус-слоган")
    COMMUNITY_TYPE_PRIVATE = 'T'
    COMMUNITY_TYPE_PUBLIC = 'P'
    COMMUNITY_TYPES = (
        (COMMUNITY_TYPE_PUBLIC, 'Публичное'),
        (COMMUNITY_TYPE_PRIVATE, 'Приватное'),
    )
    type = models.CharField(editable=False, blank=False, null=False, choices=COMMUNITY_TYPES, default='P', max_length=2)
    invites_enabled = models.BooleanField(default=True, verbose_name="Разрешить приглашения")
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Удаленное"
    )

    class Meta:
        verbose_name_plural = 'сообщества'

    @classmethod
    def is_user_with_username_member_of_community_with_name(cls, username, community_name):
        """"
        Есть ли пользователь в сообществе?
        """
        return cls.objects.filter(name=community_name, memberships__user__username=username).exists()

    @classmethod
    def is_user_with_username_administrator_of_community_with_name(cls, username, community_name):
        """"
        Администратор ли пользователь в сообществе?
        """
        return cls.objects.filter(name=community_name, memberships__user__username=username,
                                  memberships__is_administrator=True).exists()

    @classmethod
    def is_user_with_username_moderator_of_community_with_name(cls, username, community_name):
        """"
        Модератор ли пользователь в сообществе?
        """
        return cls.objects.filter(name=community_name, memberships__user__username=username,
                                  memberships__is_moderator=True).exists()

    @classmethod
    def is_user_with_username_banned_from_community_with_name(cls, username, community_name):
        """"
        Забанен ли пользователь в сообществе?
        """
        return cls.objects.filter(name=community_name, banned_users__username=username).exists()

    @classmethod
    def is_community_with_name_invites_enabled(cls, community_name):
        """"
        Нужно ли приглашение в сообщество?
        """
        return cls.objects.filter(name=community_name, invites_enabled=True).exists()

    @classmethod
    def is_community_with_name_private(cls, community_name):
        """"
        Приватное ли сообщество?
        """
        return cls.objects.filter(name=community_name, type='T').exists()

    @classmethod
    def community_with_name_exists(cls, community_name):
        """"
        Есть ли сообщество, не удаленное?
        """
        query = Q(name=community_name, is_deleted=False)
        return cls.objects.filter(query).exists()

    @classmethod
    def get_community_with_name_for_user_with_id(cls, community_name, user_id):
        """"
        Получаем сообщества для пользователя?
        """
        query = Q(name=community_name, is_deleted=False)
        query.add(~Q(banned_users__id=user_id), Q.AND)
        return cls.objects.get(query)

    @classmethod
    def search_communities_with_query(cls, query):
        """"
        Возврат списка сообществ при поиске
        """
        query = cls._make_search_communities_query(query=query)
        return cls.objects.filter(query)

    @classmethod
    def _make_search_communities_query(cls, query):
        """"
        Метод, получающий список сообществ при поиске
        """
        communities_query = Q(name__icontains=query)
        communities_query.add(Q(title__icontains=query), Q.OR)
        communities_query.add(Q(is_deleted=False), Q.AND)
        return communities_query

    @classmethod
    def get_trending_communities_for_user_with_id(cls, user_id, category_name=None):
        trending_communities_query = cls._make_trending_communities_query(category_name=category_name)
        trending_communities_query.add(~Q(banned_users__id=user_id), Q.AND)
        return cls._get_trending_communities_with_query(query=trending_communities_query)

    @classmethod
    def get_trending_communities(cls, category_name=None):
        """"
        Метод, получающий популярные сообщетсва
        """
        trending_communities_query = cls._make_trending_communities_query(category_name=category_name)
        return cls._get_trending_communities_with_query(query=trending_communities_query)

    @classmethod
    def _get_trending_communities_with_query(cls, query):
        return cls.objects.annotate(Count('memberships')).filter(query).order_by(
            '-memberships__count', '-created')

    @classmethod
    def _make_trending_communities_query(cls, category_name=None):
        trending_communities_query = Q(type=cls.COMMUNITY_TYPE_PUBLIC, is_deleted=False)
        if category_name:
            trending_communities_query.add(Q(categories__name=category_name), Q.AND)
        return trending_communities_query

    @classmethod
    def create_community(cls, name, title, creator, type=None, avatar=None, description=None,
                            rules=None, category=None,invites_enabled=None):
        """"
        Создаем сообщество и список пользователей, создателя делаем администратором
        """
        if type is Community.COMMUNITY_TYPE_PRIVATE and invites_enabled is None:
            invites_enabled = False
        else:
            invites_enabled = True

        community = cls.objects.create(title=title, name=name, creator=creator, avatar=avatar,
                                       description=description, type=type, rules=rules,
                                       invites_enabled=invites_enabled, category=category)

        CommunityMembership.create_membership(user=creator, is_administrator=True, is_moderator=False,
                                              community=community)

        community.save()
        return community

    @classmethod
    def is_name_taken(cls, name):
        """"
        Есть ли название сообщества?
        """
        return cls.objects.filter(name__iexact=name).exists()

    EXCLUDE_COMMUNITY_ADMINISTRATORS_KEYWORD = 'administrators'
    EXCLUDE_COMMUNITY_MODERATORS_KEYWORD = 'moderators'

    @classmethod
    def get_community_with_name_members(cls, community_name, members_max_id=None, exclude_keywords=None):
        """"
        Получаем всех участников сообщества
        """
        community_members_query = Q(communities_memberships__community__name=community_name)

        if members_max_id:
            community_members_query.add(Q(id__lt=members_max_id), Q.AND)

        if exclude_keywords:
            community_members_query.add(
                cls._get_exclude_members_query_for_keywords(exclude_keywords=exclude_keywords),
                Q.AND)

        return User.objects.filter(community_members_query)

    @classmethod
    def search_community_with_name_members(cls, community_name, query, exclude_keywords=None):
        """"
        Поиск по участникам группы
        """
        db_query = Q(communities_memberships__community__name=community_name)

        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)

        db_query.add(community_members_query, Q.AND)

        if exclude_keywords:
            db_query.add(
                cls._get_exclude_members_query_for_keywords(exclude_keywords=exclude_keywords),
                Q.AND)

        return User.objects.filter(db_query)

    @classmethod
    def _get_exclude_members_query_for_keywords(cls, exclude_keywords):
        query = Q()

        if cls.EXCLUDE_COMMUNITY_ADMINISTRATORS_KEYWORD in exclude_keywords:
            query.add(Q(communities_memberships__is_administrator=False), Q.AND)

        if cls.EXCLUDE_COMMUNITY_MODERATORS_KEYWORD in exclude_keywords:
            query.add(Q(communities_memberships__is_moderator=False), Q.AND)

        return query

    @classmethod
    def get_community_with_name_administrators(cls, community_name, administrators_max_id=None):
        """"
        Получаем администраторов группы
        """
        community_administrators_query = Q(communities_memberships__community__name=community_name,
                                           communities_memberships__is_administrator=True)

        if administrators_max_id:
            community_administrators_query.add(Q(communities_memberships__user__id__lt=administrators_max_id), Q.AND)

        return User.objects.filter(community_administrators_query)

    @classmethod
    def search_community_with_name_administrators(cls, community_name, query):
        """"
        Поиск по администраторам группы
        """
        db_query = Q(communities_memberships__community__name=community_name,
                     communities_memberships__is_administrator=True)

        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)

        db_query.add(community_members_query, Q.AND)

        return User.objects.filter(db_query)

    @classmethod
    def get_community_with_name_moderators(cls, community_name, moderators_max_id=None):
        """"
        Получаем модераторов группы
        """
        community_moderators_query = Q(communities_memberships__community__name=community_name,
                                       communities_memberships__is_moderator=True)

        if moderators_max_id:
            community_moderators_query.add(Q(communities_memberships__user__id__lt=moderators_max_id), Q.AND)

        return User.objects.filter(community_moderators_query)

    @classmethod
    def search_community_with_name_moderators(cls, community_name, query):
        """"
        Поиск по модераторам группы
        """
        db_query = Q(communities_memberships__community__name=community_name,
                     communities_memberships__is_moderator=True)

        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)

        db_query.add(community_members_query, Q.AND)

        return User.objects.filter(db_query)

    @classmethod
    def get_community_with_name_banned_users(cls, community_name, users_max_id):
        """"
        Получаем черный список группы
        """
        community = Community.objects.get(name=community_name)
        community_members_query = Q()

        if users_max_id:
            community_members_query.add(Q(id__lt=users_max_id), Q.AND)

        return community.banned_users.filter(community_members_query)

    @classmethod
    def search_community_with_name_banned_users(cls, community_name, query):
        """"
        Поиск по черному списку группы
        """
        community = Community.objects.get(name=community_name)
        community_banned_users_query = Q(username__icontains=query)
        community_banned_users_query.add(Q(profile__name__icontains=query), Q.OR)
        return community.banned_users.filter(community_banned_users_query)

    @property
    def members_count(self):
        """"
        кол-во участников группы
        """
        return self.memberships.all().count()

    def get_staff_members(self):
        """"
        Получаем весь персонал группы
        """
        User = get_user_model()
        staff_members_query = Q(communities_memberships__community_id=self.pk)
        staff_members_query.add(
            Q(communities_memberships__is_administrator=True) | Q(communities_memberships__is_moderator=True), Q.AND)
        return User.objects.filter(staff_members_query)

    def is_private(self):
        """"
        Группа приватная?
        """
        return self.type is self.COMMUNITY_TYPE_PRIVATE

    def update(self, title=None, name=None, description=None, color=None, type=None,
               user_adjective=None,
               users_adjective=None, rules=None, communitysubcategory_names=None, invites_enabled=None):
        """"
        Обновление группы
        """

        if name:
            self.name = name.lower()
        if title:
            self.title = title
        if type:
            self.type = type
        if description is not None:
            self.description = description
        if rules is not None:
            self.rules = rules
        if invites_enabled is not None:
            self.invites_enabled = invites_enabled
        self.save()

    def add_moderator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = True
        user_membership.save()
        return user_membership

    def remove_moderator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.save()
        return user_membership

    def add_administrator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_administrator = True
        user_membership.save()
        return user_membership

    def remove_administrator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_administrator = False
        user_membership.save()
        return user_membership

    def add_member(self, user):
        user_membership = CommunityMembership.create_membership(user=user, community=self)
        return user_membership

    def remove_member(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.delete()

    def create_invite(self, creator, invited_user):
        """"
        Создание приглащения в группу
        """
        CommunityInvite = get_community_invite_model()
        return CommunityInvite.create_community_invite(creator=creator, invited_user=invited_user, community=self)

    def create_user_ban_log(self, source_user, target_user):
        return self._create_log(action_type='B',
                                source_user=source_user,
                                target_user=target_user)

    def create_user_unban_log(self, source_user, target_user):
        return self._create_log(action_type='U',
                                source_user=source_user,
                                target_user=target_user)

    def create_add_administrator_log(self, source_user, target_user):
        return self._create_log(action_type='AA',
                                source_user=source_user,
                                target_user=target_user)

    def create_remove_administrator_log(self, source_user, target_user):
        return self._create_log(action_type='RA',
                                source_user=source_user,
                                target_user=target_user)

    def create_add_moderator_log(self, source_user, target_user):
        return self._create_log(action_type='AM',
                                source_user=source_user,
                                target_user=target_user)

    def create_remove_moderator_log(self, source_user, target_user):
        return self._create_log(action_type='RM',
                                source_user=source_user,
                                target_user=target_user)

    def create_remove_post_log(self, source_user, target_user):
        return self._create_log(action_type='RP',
                                source_user=source_user,
                                target_user=target_user)

    def create_remove_post_comment_log(self, source_user, target_user):
        return self._create_log(action_type='RPC',
                                source_user=source_user,
                                target_user=target_user)

    def create_remove_post_comment_reply_log(self, source_user, target_user):
        return self._create_log(action_type='RPCR',
                                source_user=source_user,
                                target_user=target_user)

    def create_disable_post_comments_log(self, source_user, target_user, post):
        return self._create_log(action_type='DPC',
                                post=post,
                                source_user=source_user,
                                target_user=target_user)

    def create_enable_post_comments_log(self, source_user, target_user, post):
        return self._create_log(action_type='EPC',
                                post=post,
                                source_user=source_user,
                                target_user=target_user)

    def create_open_post_log(self, source_user, target_user, post):
        return self._create_log(action_type='OP',
                                post=post,
                                source_user=source_user,
                                target_user=target_user)

    def create_close_post_log(self, source_user, target_user, post):
        return self._create_log(action_type='CP',
                                post=post,
                                source_user=source_user,
                                target_user=target_user)

    def _create_log(self, action_type, source_user, target_user, post=None):
        return CommunityModeratorUserActionLog.create_community_log(community=self,
                                                                    post=post,
                                                                    target_user=target_user,
                                                                    action_type=action_type,
                                                                    source_user=source_user)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.name = self.name.lower()
        return super(Community, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CommunityMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities_memberships', null=False, blank=False, verbose_name="Члены сообщества")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='memberships', null=False, blank=False, verbose_name="Сообщество")
    is_administrator = models.BooleanField(default=False, verbose_name="Это администратор")
    is_moderator = models.BooleanField(default=False, verbose_name="Это модератор")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create_membership(cls, user, community, is_administrator=False, is_moderator=False):
        membership = cls.objects.create(user=user, community=community, is_administrator=is_administrator,
                                        is_moderator=is_moderator)

        return membership

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(CommunityMembership, self).save(*args, **kwargs)


class CommunityLog(models.Model):
    source_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=False, blank=False, verbose_name="Кто модерирует")
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True, blank=False, verbose_name="Кого модерируют")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', null=True, blank=True, verbose_name="Пост")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='logs', null=False, blank=False, verbose_name="Сообщество")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создан")

    ACTION_TYPES = (
        ('B', 'Заблокировать'),
        ('U', 'Разблокировать'),
        ('AM', 'Добавить модератора'),
        ('RM', 'Удалить модератора'),
        ('AA', 'Добавить администратора'),
        ('RA', 'Удалить администратора'),
        ('OP', 'Открыть пост'),
        ('CP', 'Закрыть пост'),
        ('RP', 'Удалить пост'),
        ('RPC', 'Удалить комментарий к посту'),
        ('DPC', 'Отключить комментарии'),
        ('EPC', 'Включить комментарии'),
    )
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)

    @classmethod
    def create_community_log(cls, community, action_type, source_user, target_user, post=None):
        return cls.objects.create(community=community, action_type=action_type, source_user=source_user,
                                  target_user=target_user, post=post)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(CommunityLog, self).save(*args, **kwargs)


class CommunityInvite(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities_invites', null=False,blank=False, verbose_name="Кто приглашает в сообщество")
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities_invites', null=False, blank=False, verbose_name="Кого приглашают в сообщество")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='invites', null=False, blank=False, verbose_name="Сообщество")

    @classmethod
    def create_community_invite(cls, creator, invited_user, community):
        return cls.objects.create(creator=creator, invited_user=invited_user, community=community)

    @classmethod
    def is_user_with_username_invited_to_community_with_name(cls, username, community_name):
        return cls.objects.filter(community__name=community_name, invited_user__username=username).exists()
