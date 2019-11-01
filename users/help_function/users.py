def _make_linked_users_query(self):
    """ получаем всех подписчиков и друзей пользователя """

    linked_users_query = Q(circles__connections__target_connection__user_id=self.pk,
                           circles__connections__target_connection__circles__isnull=False)

    followers_query = self._make_followers_query()

    linked_users_query.add(followers_query, Q.OR)

    linked_users_query.add(Q(is_deleted=False), Q.AND)

    return linked_users_query


def _make_blocked_users_query(self, max_id=None):
    """ получаем черный список пользователя """
    blocked_users_query = Q(blocked_by_users__blocker_id=self.pk, )

    if max_id:
        blocked_users_query.add(Q(id__lt=max_id), Q.AND)

    return blocked_users_query


def _can_see_post(self, item):
    """ получаем записи, которые создал пользователь """
    post_query = self._make_get_post_with_id_query_for_user(item.creator, item_id=item.pk)
    profile_posts = Item.objects.filter(post_query)
    return profile_posts.exists()


def _can_see_community_post(self, community, item):
    """ получаем записи сщщбщества, которые создал пользователь """
    if item.creator_id == self.pk:
        return True
    community_posts_query = self._make_get_community_with_id_posts_query(community=community)
    community_posts_query.add(Q(pk=item.pk), Q.AND)
    return Item.objects.filter(community_posts_query).exists()


def unblock_user_with_username(self, username):
    user = User.objects.get(username=username)
    return self.unblock_user_with_id(user_id=user.pk)
def unblock_user_with_id(self, user_id):
    check_can_unblock_user_with_id(user=self, user_id=user_id)
    self.user_blocks.filter(blocked_user_id=user_id).delete()
    return User.objects.get(pk=user_id)


def block_user_with_username(self, username):
    user = User.objects.get(username=username)
    return self.block_user_with_id(user_id=user.pk)

def block_user_with_id(self, user_id):
    check_can_block_user_with_id(user=self, user_id=user_id)

    if self.is_connected_with_user_with_id(user_id=user_id):
        # This does unfollow too
        self.disconnect_from_user_with_id(user_id=user_id)
    elif self.is_following_user_with_id(user_id=user_id):
        self.unfollow_user_with_id(user_id=user_id)

    user_to_block = User.objects.get(pk=user_id)
    if user_to_block.is_following_user_with_id(user_id=self.pk):
        user_to_block.unfollow_user_with_id(self.pk)

    UserBlock.create_user_block(blocker_id=self.pk, blocked_user_id=user_id)

    return user_to_block


def get_connection_for_user_with_id(self, user_id):
    return self.connections.get(target_connection__user_id=user_id)

def get_follow_for_user_with_id(self, user_id):
    return self.follows.get(followed_user_id=user_id)


def get_posts_for_user_with_username(self, username, max_id=None, min_id=None):
    user = User.objects.get(username=username)
    return self.get_posts_for_user(user=user, max_id=max_id, min_id=min_id)

def get_posts_for_user(self, user, max_id=None, min_id=None):

    user_query = Q(creator_id=user.pk)

    exclude_reported_and_approved_posts_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)

    exclude_reported_posts_query = ~Q(moderated_object__reports__reporter_id=self.pk)

    cursor_scrolling_query = Q()

    if max_id:
        cursor_scrolling_query = Q(id__lt=max_id)
    elif min_id:
        cursor_scrolling_query = Q(id__gt=min_id)

    exclude_blocked_posts_query = ~Q(Q(creator__blocked_by_users__blocker_id=self.pk) | Q(
        creator__user_blocks__blocked_user_id=self.pk))

    exclude_deleted_posts_query = Q(is_deleted=False, status=Post.STATUS_PUBLISHED)

        # Get user world circle posts

    world_circle_posts_query = Q(creator__id=user.pk)

    world_circle_posts = Item.objects.filter(
        user_query &
        world_circle_posts_query &
        exclude_deleted_posts_query &
        exclude_blocked_posts_query &
        exclude_reported_posts_query &
        exclude_reported_and_approved_posts_query &
        cursor_scrolling_query
    )

    # Get user community posts
    community_posts_query = Q(creator__pk=user.pk, community__isnull=False, is_closed=False)
    exclude_private_community_posts_query = Q(community__type=Community.COMMUNITY_TYPE_PUBLIC) | Q(
        community__memberships__user__id=self.pk)

    community_posts = Item.objects.filter(
        user_query &
        community_posts_query &
        exclude_private_community_posts_query &
        exclude_deleted_posts_query &
        exclude_blocked_posts_query &
        exclude_reported_posts_query &
        exclude_reported_and_approved_posts_query &
        cursor_scrolling_query
    )

    connection_circles_posts = Item.objects.filter(
        user_query &
        connection_circles_query &
        exclude_deleted_posts_query &
        exclude_blocked_posts_query &
        exclude_reported_posts_query &
        exclude_reported_and_approved_posts_query &
        cursor_scrolling_query
    )

    if user.has_profile_community_posts_visible():
        results = world_circle_posts.union(community_posts, connection_circles_posts)
    else:
        results = world_circle_posts.union(connection_circles_posts)

    return results


def get_posts(self, max_id=None):
    """
    Получить все посты пользователя
    """
    posts_query = Q(creator_id=self.id, is_deleted=False, status=Item.STATUS_PUBLISHED)

    exclude_reported_and_approved_posts_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)

    posts_query.add(exclude_reported_and_approved_posts_query, Q.AND)

    if not self.has_profile_community_posts_visible():
        posts_query.add(Q(community__isnull=True), Q.AND)

    if max_id:
        posts_query.add(Q(id__lt=max_id), Q.AND)

    posts = Post.objects.filter(posts_query)

    return posts


def search_users_with_query(self, query):
    users_query = self._make_search_users_query(query=query)

    return User.objects.filter(users_query)

def _make_search_users_query(self, query):
    users_query = self._make_users_query()

    search_users_query = Q(username__icontains=query)
    search_users_query.add(Q(profile__name__icontains=query), Q.OR)

    users_query.add(search_users_query, Q.AND)
    return users_query

def _make_users_query(self):
    users_query = Q(is_deleted=False)
    users_query.add(~Q(blocked_by_users__blocker_id=self.pk) & ~Q(user_blocks__blocked_user_id=self.pk),
                    Q.AND)
    return users_query

def get_linked_users(self, max_id=None):
    # All users which are connected with us and we have accepted by adding
    # them to a circle
    linked_users_query = self._make_linked_users_query()

    if max_id:
        linked_users_query.add(Q(id__lt=max_id), Q.AND)

    return User.objects.filter(linked_users_query).distinct()

def search_linked_users_with_query(self, query):
    linked_users_query = self._make_linked_users_query()

    names_query = Q(username__icontains=query)
    names_query.add(Q(profile__name__icontains=query), Q.OR)

    linked_users_query.add(names_query, Q.AND)

    return User.objects.filter(linked_users_query).distinct()

def get_blocked_users(self, max_id=None):
    blocked_users_query = self._make_blocked_users_query(max_id=max_id)

    return User.objects.filter(blocked_users_query).distinct()

def search_blocked_users_with_query(self, query):
    blocked_users_query = self._make_blocked_users_query()

    names_query = Q(username__icontains=query)
    names_query.add(Q(profile__name__icontains=query), Q.OR)

    blocked_users_query.add(names_query, Q.AND)

    return User.objects.filter(blocked_users_query).distinct()

def search_top_posts_excluded_communities_with_query(self, query):

    excluded_communities_search_query = Q(user=self)
    excluded_communities_search_query.add((Q(community__title__icontains=query) |
                                           Q(community__name__icontains=query)), Q.AND)

    return TopPostCommunityExclusion.objects.filter(excluded_communities_search_query)


def has_post(self, item):
    return item.creator_id == self.pk

def has_muted_post_with_id(self, item_id):
    return self.post_mutes.filter(item_id=item_id).exists()

def has_muted_post_comment_with_id(self, post_comment_id):
    return self.post_comment_mutes.filter(post_comment_id=post_comment_id).exists()

def has_blocked_user_with_id(self, user_id):
    return self.user_blocks.filter(blocked_user_id=user_id).exists()


def update_notifications_settings(self, post_comment_notifications=None, post_reaction_notifications=None,
                                  follow_notifications=None, connection_request_notifications=None,
                                  connection_confirmed_notifications=None,
                                  community_invite_notifications=None,
                                  post_comment_reaction_notifications=None,
                                  post_comment_reply_notifications=None,
                                  post_comment_user_mention_notifications=None,
                                  post_user_mention_notifications=None,
                                  ):

    notifications_settings = self.notifications_settings

    notifications_settings.update(
        post_comment_notifications=post_comment_notifications,
        post_reaction_notifications=post_reaction_notifications,
        follow_notifications=follow_notifications,
        connection_request_notifications=connection_request_notifications,
        connection_confirmed_notifications=connection_confirmed_notifications,
        community_invite_notifications=community_invite_notifications,
        post_comment_reaction_notifications=post_comment_reaction_notifications,
        post_comment_reply_notifications=post_comment_reply_notifications,
        post_comment_user_mention_notifications=post_comment_user_mention_notifications,
        post_user_mention_notifications=post_user_mention_notifications,
    )
    return notifications_settings


def soft_delete(self):
    for item in self.item.all().iterator():
        item.soft_delete()

    for community in self.created_communities.all().iterator():
        community.soft_delete()

    self.is_deleted = True
    self.save()

def unsoft_delete(self):
    for item in self.item.all.iterator():
        item.unsoft_delete()

    for community in self.created_communities.all().iterator():
        community.unsoft_delete()

    self.is_deleted = False
    self.save()


def count_public_posts(self):
    """
    Count how many public posts has the user created
    :return:
    """

    return self.item.filter(circles__id=world_circle_id).count()

def count_posts_for_user_with_id(self, id):
    """
    Count how many posts has the user created relative to another user
    :param id:
    :return: count
    """
    user = User.objects.get(pk=id)
    if user.is_connected_with_user_with_id(self.pk):
        count = user.get_posts_for_user_with_username(username=self.username).count()
    else:
        count = self.count_public_posts()
    return count

def count_followers(self):
    return Follow.objects.filter(followed_user__id=self.pk).count()

def count_following(self):
    return self.follows.count()

def count_connections(self):
    return self.connections.count()

 def count_posts(self):
    return self.posts.count()
