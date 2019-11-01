def get_top_posts(self, max_id=None, min_id=None, exclude_joined_communities=False):
    """
    Возвращает верхние сообщения (только для сообществ) для аутентифицированных пользователей, исключая сообщения зарегистрированных, закрытых и заблокированных пользователей
    """
    posts_select_related = ('item__creator', 'item__creator__profile', 'item__community', 'item__image')

    posts_only = ('id',
                  'item__text', 'item__id', 'item__uuid', 'item__created', 'item__image',
                  'item__creator__username', 'item__creator__id', 'item__creator__profile__name',
                  'item__creator__profile__avatar',
                  'item__creator__profile__id', 'item__community__id', 'item__community__name',
                  'item__community__avatar',
                  'item__community__title')

    reported_posts_exclusion_query = ~Q(item__moderated_object__reports__reporter_id=self.pk)
    excluded_communities_query = ~Q(item__community__top_posts_community_exclusions__user=self.pk)

    top_community_posts_query = Q(item__is_closed=False,
                                  item__is_deleted=False,
                                  item__status=Item.STATUS_PUBLISHED)

    top_community_posts_query.add(~Q(Q(item__creator__blocked_by_users__blocker_id=self.pk) | Q(
        item__creator__user_blocks__blocked_user_id=self.pk)), Q.AND)
    top_community_posts_query.add(Q(item__community__type=Community.COMMUNITY_TYPE_PUBLIC), Q.AND)
    top_community_posts_query.add(~Q(item__community__banned_users__id=self.pk), Q.AND)

    if max_id:
        top_community_posts_query.add(Q(id__lt=max_id), Q.AND)
    elif min_id:
        top_community_posts_query.add(Q(id__gt=min_id), Q.AND)

    top_community_posts_query.add(~Q(item__moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)

    if exclude_joined_communities:
        # exclude communities the user is a member of
        exclude_joined_communities_query = ~Q(item__community__memberships__user__id=self.pk)
        top_community_posts_query.add(exclude_joined_communities_query, Q.AND)

    top_community_posts_query.add(reported_posts_exclusion_query, Q.AND)
    top_community_posts_query.add(excluded_communities_query, Q.AND)

    top_community_posts_queryset = TopPost.objects.select_related(*posts_select_related).prefetch_related(
        *posts_prefetch_related).only(*posts_only).filter(top_community_posts_query)

    return top_community_posts_queryset


def exclude_community_from_top_posts(self, community):
    check_can_exclude_community(user=self, community=community)

    TopPostCommunityExclusion = get_top_post_community_exclusion_model()
    top_post_community_exclusion = TopPostCommunityExclusion(
        user=self,
        community=community
    )
    self.top_posts_community_exclusions.add(top_post_community_exclusion, bulk=False)

def exclude_community_with_name_from_top_posts(self, community_name):
    community_to_exclude = Community.objects.get(name=community_name)
    self.exclude_community_from_top_posts(community_to_exclude)

def remove_exclusion_for_community_from_top_posts(self, community):
        check_can_remove_exclusion_for_community(user=self, community=community)

    TopPostCommunityExclusion.objects.get(user=self, community=community).delete()

def remove_exclusion_for_community_with_name_from_top_posts(self, community_name):
    community = Community.objects.get(name=community_name)
    self.remove_exclusion_for_community_from_top_posts(community)


def get_top_posts(self, max_id=None, min_id=None, exclude_joined_communities=False):
    """
    Gets top posts (communities only) for authenticated user excluding reported, closed, blocked users posts
    """

    posts_select_related = ('item__creator', 'item__creator__profile', 'item__community', 'item__image')

    posts_only = ('id',
                  'item__text', 'item__id', 'item__uuid', 'item__image',
                  'item__creator__username', 'item__creator__id', 'item__creator__profile__name',
                  'item__creator__profile__avatar',
                  'item__creator__profile__id', 'item__community__id', 'item__community__name',
                  'item__community__avatar',
                  'item__community__color', 'item__community__title')

    reported_posts_exclusion_query = ~Q(item__moderated_object__reports__reporter_id=self.pk)
    excluded_communities_query = ~Q(item__community__top_posts_community_exclusions__user=self.pk)

    top_community_posts_query = Q(item__is_closed=False,
                                  item__is_deleted=False,
                                  item__status=Item.STATUS_PUBLISHED)

    top_community_posts_query.add(~Q(Q(item__creator__blocked_by_users__blocker_id=self.pk) | Q(
        item__creator__user_blocks__blocked_user_id=self.pk)), Q.AND)
    top_community_posts_query.add(Q(item__community__type=Community.COMMUNITY_TYPE_PUBLIC), Q.AND)
    top_community_posts_query.add(~Q(item__community__banned_users__id=self.pk), Q.AND)

    if max_id:
        top_community_posts_query.add(Q(id__lt=max_id), Q.AND)
    elif min_id:
        top_community_posts_query.add(Q(id__gt=min_id), Q.AND)

    top_community_posts_query.add(~Q(item__moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)

    if exclude_joined_communities:
        # exclude communities the user is a member of
        exclude_joined_communities_query = ~Q(item__community__memberships__user__id=self.pk)
        top_community_posts_query.add(exclude_joined_communities_query, Q.AND)

    top_community_posts_query.add(reported_posts_exclusion_query, Q.AND)
    top_community_posts_query.add(excluded_communities_query, Q.AND)

    top_community_posts_queryset = TopPost.objects.select_related(*posts_select_related).prefetch_related(
        *posts_prefetch_related).only(*posts_only).filter(top_community_posts_query)

    return top_community_posts_queryset


def get_closed_posts_for_community_with_name(self, community_name, max_id=None):
    check_can_get_closed_posts_for_community_with_name(user=self, community_name=community_name)
    community = Community.objects.get(name=community_name)

    posts_query = Q(community__id=community.pk, is_closed=True)

    if max_id:
        posts_query.add(Q(id__lt=max_id), Q.AND)
    profile_posts = Item.objects.filter(posts_query).distinct()

    return profile_posts


def get_posts_for_community_with_name(self, community_name, max_id=None):
    check_can_get_posts_for_community_with_name(user=self, community_name=community_name)

    community = Community.objects.get(name=community_name)

    # Мы не хотим видеть закрытые сообщения на временной шкале сообщества, если мы являемся сотрудниками
    community_posts_query = self._make_get_community_with_id_posts_query(community=community,
                                                                             include_closed_posts_for_staff=False)

    if max_id:
        community_posts_query.add(Q(id__lt=max_id), Q.AND)

    profile_posts = Item.objects.filter(community_posts_query).distinct()

    return profile_posts


def create_community_post(self, community_name, text=None, image=None, video=None, created=None, is_draft=False):
    check_can_post_to_community_with_name(user=self, community_name=community_name)
    item = Item.create_post(text=text, creator=self, community_name=community_name, image=image, video=video,
                            created=created, is_draft=is_draft)

    return item


def get_trending_communities(self, category_name=None):
    return Community.get_trending_communities_for_user_with_id(user_id=self.pk, category_name=category_name)

def search_communities_with_query(self, query):
    return Community.search_communities_with_query(query)

def get_community_with_name(self, community_name):
    check_can_get_community_with_name(user=self, community_name=community_name)
    return Community.get_community_with_name_for_user_with_id(community_name=community_name, user_id=self.pk)

def get_joined_communities(self):
    return Community.objects.filter(memberships__user=self)

def search_joined_communities_with_query(self, query):
    joined_communities_query = Q(memberships__user=self)
    joined_communities_name_query = Q(name__icontains=query)
    joined_communities_query.add(joined_communities_name_query, Q.AND)
    return Community.objects.filter(joined_communities_query)


def search_top_posts_excluded_communities_with_query(self, query):

    excluded_communities_search_query = Q(user=self)
    excluded_communities_search_query.add((community__name__icontains=query), Q.AND)

    return TopPostCommunityExclusion.objects.filter(excluded_communities_search_query)

def get_top_posts_community_exclusions(self):
    top_posts_community_exclusions = TopPostCommunityExclusion.objects \
        .select_related('community') \
        .filter(user=self)

    return top_posts_community_exclusions


def get_community_with_name_banned_users(self, community_name, max_id):
    check_can_get_community_with_name_banned_users(
        user=self,
        community_name=community_name)

    return Community.get_community_with_name_banned_users(community_name=community_name, users_max_id=max_id)

def search_community_with_name_banned_users(self, community_name, query):
    check_can_get_community_with_name_banned_users(
        user=self,
        community_name=community_name)

    return Community.search_community_with_name_banned_users(community_name=community_name, query=query)

def ban_user_with_username_from_community_with_name(self, username, community_name):
    check_can_ban_user_with_username_from_community_with_name(user=self, username=username,
                                                              community_name=community_name)

    community_to_ban_user_from = Community.objects.get(name=community_name)
    user_to_ban = User.objects.get(username=username)

    if user_to_ban.is_member_of_community_with_name(community_name=community_name):
        user_to_ban.leave_community_with_name(community_name=community_name)

    community_to_ban_user_from.banned_users.add(user_to_ban)
    community_to_ban_user_from.create_user_ban_log(source_user=self, target_user=user_to_ban)

    return community_to_ban_user_from

def unban_user_with_username_from_community_with_name(self, username, community_name):
    check_can_unban_user_with_username_from_community_with_name(user=self, username=username,
                                                                community_name=community_name)

    community_to_unban_user_from = Community.objects.get(name=community_name)
    user_to_unban = User.objects.get(username=username)

    community_to_unban_user_from.banned_users.remove(user_to_unban)
    community_to_unban_user_from.create_user_unban_log(source_user=self, target_user=user_to_unban)

    return community_to_unban_user_from


def get_community_with_name_administrators(self, community_name, max_id):
    check_can_get_community_with_name_administrators(
        user=self,
        community_name=community_name)
    return Community.get_community_with_name_administrators(community_name=community_name,
                                                            administrators_max_id=max_id)

def search_community_with_name_administrators(self, community_name, query):
    check_can_get_community_with_name_administrators(
        user=self,
        community_name=community_name)
    return Community.search_community_with_name_administrators(community_name=community_name, query=query)

def add_administrator_with_username_to_community_with_name(self, username, community_name):
    check_can_add_administrator_with_username_to_community_with_name(
        user=self,
        username=username,
        community_name=community_name)

    community_to_add_administrator_to = Community.objects.get(name=community_name)
    user_to_add_as_administrator = User.objects.get(username=username)

    community_to_add_administrator_to.add_administrator(user_to_add_as_administrator)
    community_to_add_administrator_to.create_add_administrator_log(source_user=self,
                                                                   target_user=user_to_add_as_administrator)

    if user_to_add_as_administrator.is_moderator_of_community_with_name(community_name=community_name):
        self.remove_moderator_with_username_from_community_with_name(username=username,
                                                                         community_name=community_name)

    return community_to_add_administrator_to

def remove_administrator_with_username_from_community_with_name(self, username, community_name):
    check_can_remove_administrator_with_username_to_community_with_name(
        user=self,
        username=username,
        community_name=community_name)

    community_to_remove_administrator_from = Community.objects.get(name=community_name)
    user_to_remove_as_administrator = User.objects.get(username=username)

    community_to_remove_administrator_from.remove_administrator(user_to_remove_as_administrator)
    community_to_remove_administrator_from.create_remove_administrator_log(source_user=self,
                                                                           target_user=user_to_remove_as_administrator)

    return community_to_remove_administrator_from

def get_community_with_name_moderators(self, community_name, max_id):
    check_can_get_community_with_name_moderators(
        user=self,
        community_name=community_name)
    return Community.get_community_with_name_moderators(community_name=community_name,
                                                        moderators_max_id=max_id)

def search_community_with_name_moderators(self, community_name, query):
    check_can_get_community_with_name_moderators(
        user=self,
        community_name=community_name)

    return Community.search_community_with_name_moderators(community_name=community_name, query=query)

def add_moderator_with_username_to_community_with_name(self, username, community_name):
    check_can_add_moderator_with_username_to_community_with_name(
        user=self,
        username=username,
        community_name=community_name)

    community_to_add_moderator_to = Community.objects.get(name=community_name)
    user_to_add_as_moderator = User.objects.get(username=username)

    community_to_add_moderator_to.add_moderator(user_to_add_as_moderator)

    community_to_add_moderator_to.create_add_moderator_log(source_user=self,
                                                           target_user=user_to_add_as_moderator)

    return community_to_add_moderator_to

def remove_moderator_with_username_from_community_with_name(self, username, community_name):
    check_can_remove_moderator_with_username_to_community_with_name(user=self,username=username,community_name=community_name)

    community_to_remove_moderator_from = Community.objects.get(name=community_name)
    user_to_remove_as_moderator = User.objects.get(username=username)

    community_to_remove_moderator_from.remove_moderator(user_to_remove_as_moderator)
    community_to_remove_moderator_from.create_remove_moderator_log(source_user=self,target_user=user_to_remove_as_moderator)

    return community_to_remove_moderator_from


def delete_community_with_name_cover(self, community_name):
    check_can_update_community_with_name(user=self, community_name=community_name)

    community_to_delete_cover_from = Community.objects.get(name=community_name)

    delete_file_field(community_to_delete_cover_from.cover)
    community_to_delete_cover_from.cover = None
    community_to_delete_cover_from.save()
    return community_to_delete_cover_from

def get_community_with_name_members(self, community_name, max_id=None, exclude_keywords=None):
    check_can_get_community_with_name_members(
        user=self,
        community_name=community_name)

    return Community.get_community_with_name_members(community_name=community_name, members_max_id=max_id,
                                                     exclude_keywords=exclude_keywords)

def search_community_with_name_members(self, community_name, query, exclude_keywords=None):
    check_can_get_community_with_name_members(
        user=self,
        community_name=community_name)

    return Community.search_community_with_name_members(community_name=community_name, query=query,
                                                        exclude_keywords=exclude_keywords)

def join_community_with_name(self, community_name):
    check_can_join_community_with_name(
        user=self,
        community_name=community_name)

    community_to_join = Community.objects.get(name=community_name)
    community_to_join.add_member(self)

        # Clean up any invites
    CommunityInvite.objects.filter(community__name=community_name, invited_user__username=self.username).delete()

    return community_to_join

def leave_community_with_name(self, community_name):
    check_can_leave_community_with_name(
        user=self,
        community_name=community_name)

    community_to_leave = Community.objects.get(name=community_name)

    if self.has_favorite_community_with_name(community_name):
        self.unfavorite_community_with_name(community_name=community_name)

    community_to_leave.remove_member(self)

    return community_to_leave

def invite_user_with_username_to_community_with_name(self, username, community_name):
    check_can_invite_user_with_username_to_community_with_name(user=self, username=username,
                                                                   community_name=community_name)

    community_to_invite_user_to = Community.objects.get(name=community_name)
    user_to_invite = User.objects.get(username=username)

    community_invite = community_to_invite_user_to.create_invite(creator=self, invited_user=user_to_invite)

    self._create_community_invite_notification(community_invite)
    self._send_community_invite_push_notification(community_invite)

    return community_invite

def uninvite_user_with_username_to_community_with_name(self, username, community_name):
    check_can_uninvite_user_with_username_to_community_with_name(user=self, username=username,
                                                                 community_name=community_name)

    community_invite = self.created_communities_invites.get(invited_user__username=username, creator=self,
                                                                community__name=community_name)
    uninvited_user = community_invite.invited_user
    community_invite.delete()

    return uninvited_user


def create_community(self, name, type, categories_names, description=None, rules=None,
                         avatar=None, cover=None, invites_enabled=None):
    check_can_create_community_with_name(user=self, name=name)

    community = Community.create_community(name=name, creator=self, description=description,
                                           rules=rules, cover=cover, type=type, avatar=avatar,
                                           categories_names=categories_names,
                                           invites_enabled=invites_enabled)

    return community

def delete_community(self, community):
    return self.delete_community_with_name(community.name)

def delete_community_with_name(self, community_name):
    check_can_delete_community_with_name(user=self, community_name=community_name)

    community = Community.objects.get(name=community_name)

    community.delete()

def update_community(self, community, name=None, description=None, color=None, type=None,
                     user_adjective=None,
                     users_adjective=None, rules=None):
    return self.update_community_with_name(community.name, name=name, description=description,
                                           type=type, rules=rules)

def update_community_with_name(self, community_name, name=None, description=None, type=None,
                               rules=None, categories_names=None,
                               invites_enabled=None):
    check_can_update_community_with_name(user=self, community_name=community_name)
    check_community_data(user=self, name=name)

    community_to_update = Community.objects.get(name=community_name)

    community_to_update.update(name=name, description=description,
                               type=type, rules=rules, categories_names=categories_names,
                               invites_enabled=invites_enabled)

    return community_to_update

def update_community_with_name_avatar(self, community_name, avatar):
    check_can_update_community_with_name(user=self, community_name=community_name)
    check_community_data(user=self, avatar=avatar)

    community_to_update_avatar_from = Community.objects.get(name=community_name)
    community_to_update_avatar_from.avatar = avatar

    community_to_update_avatar_from.save()

    return community_to_update_avatar_from

def delete_community_with_name_avatar(self, community_name):
    check_can_update_community_with_name(user=self, community_name=community_name)

    community_to_delete_avatar_from = Community.objects.get(name=community_name)
    delete_file_field(community_to_delete_avatar_from.avatar)
    community_to_delete_avatar_from.avatar = None
    community_to_delete_avatar_from.save()
    return community_to_delete_avatar_from

def update_community_with_name_cover(self, community_name, cover):
    check_can_update_community_with_name(user=self, community_name=community_name)
    check_community_data(user=self, cover=cover)

    community_to_update_cover_from = Community.objects.get(name=community_name)

    community_to_update_cover_from.cover = cover

    community_to_update_cover_from.save()

    return community_to_update_cover_from


def favorite_community_with_name(self, community_name):
    check_can_favorite_community_with_name(user=self, community_name=community_name)

    community_to_favorite = Community.objects.get(name=community_name)

    self.favorite_communities.add(community_to_favorite)

    return community_to_favorite

def unfavorite_community_with_name(self, community_name):
    check_can_unfavorite_community_with_name(user=self, community_name=community_name)

    community_to_unfavorite = Community.objects.get(name=community_name)

    self.favorite_communities.remove(community_to_unfavorite)

    return community_to_unfavorite


def has_profile_community_posts_visible(self):
    return self.profile.community_posts_visible


def has_favorite_community_with_name(self, community_name):
    return self.favorite_communities.filter(name=community_name).exists()

def has_excluded_community_with_name(self, community_name):
    return self.top_posts_community_exclusions.filter(community__name=community_name).exists()


def has_invited_user_with_username_to_community_with_name(self, username, community_name):
    return self.created_communities_invites.filter(invited_user__username=username,
                                                   community__name=community_name).exists()
