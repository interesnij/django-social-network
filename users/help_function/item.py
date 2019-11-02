def search_participants_for_post_with_uuid(self, item_uuid, query):
        item = Item.objects.get(uuid=post_uuid)
        return self.search_participants_for_post(item=item, query=query)

def search_participants_for_post(self, item, query):
    self.can_see_post(item=item)
        # В будущем это должно поставить участников post выше глобального поиска
        # Банкомат совмещать должность участников и глобальных результатов запроса в убийстве перфорация
        # Поэтому пока использует глобальный поиск
    search_users_query = self._make_search_users_query(query=query)
    return User.objects.filter(search_users_query)

def get_participants_for_post_with_uuid(self, item_uuid):
    item = Item.objects.get(uuid=item_uuid)
    return self.get_participants_for_post(item=item)

def get_participants_for_post(self, item):
    self.can_see_post(item=item)
    return item.get_participants()


def _make_get_post_with_id_query_for_user(self, user, post_id):
    posts_query = self._make_get_posts_query_for_user(user)
    posts_query.add(Q(id=post_id), Q.AND)
    return posts_query

def _make_get_posts_query_for_user(self, user, max_id=None):
    """ получаем все записи, которые создал пользователь """

    posts_query = Q(creator_id=user.pk, is_deleted=False, status=Post.STATUS_PUBLISHED)

    posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=self.pk) | Q(
        creator__user_blocks__blocked_user_id=self.pk)), Q.AND)

    if max_id:
        posts_query.add(Q(id__lt=max_id), Q.AND)

    posts_query.add(~Q(moderated_object__reports__reporter_id=self.pk), Q.AND)

    return posts_query


def _make_get_reactions_for_post_query(self, item, max_id=None, emoji_id=None):
    """ получаем реакции записи с пристрастием """
    reactions_query = Q(item_id=item.pk)

    # Если реакции частные, возвращайте только собственные реакции
    if not item.public_reactions:
        reactions_query = Q(reactor_id=self.pk)

    post_community = item.community

    if post_community:
        if not self.is_staff_of_community_with_name(community_name=post_community.name):
            blocked_users_query = ~Q(Q(reactor__blocked_by_users__blocker_id=self.pk) | Q(
                reactor__user_blocks__blocked_user_id=self.pk))
            blocked_users_query_staff_members = Q(
                reactor__communities_memberships__community_id=post_community.pk)
            blocked_users_query_staff_members.add(Q(reactor__communities_memberships__is_administrator=True) | Q(
                reactor__communities_memberships__is_moderator=True), Q.AND)

            blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
            reactions_query.add(blocked_users_query, Q.AND)
    else:
        blocked_users_query = ~Q(Q(reactor__blocked_by_users__blocker_id=self.pk) | Q(
            reactor__user_blocks__blocked_user_id=self.pk))
        reactions_query.add(blocked_users_query, Q.AND)

    if max_id:
        reactions_query.add(Q(id__lt=max_id), Q.AND)

    if emoji_id:
        reactions_query.add(Q(emoji_id=emoji_id), Q.AND)

    return reactions_query


def _make_get_reactions_for_post_comment_query(self, post_comment, max_id=None, emoji_id=None):
    """ получаем реакции комментария записи с пристрастием """
    reactions_query = Q(post_comment_id=post_comment.pk)

    post_comment_community = post_comment.item.community

    if post_comment_community:
        if not self.is_staff_of_community_with_name(community_name=post_comment_community.name):
            blocked_users_query = ~Q(Q(reactor__blocked_by_users__blocker_id=self.pk) | Q(
                reactor__user_blocks__blocked_user_id=self.pk))
            blocked_users_query_staff_members = Q(
                reactor__communities_memberships__community_id=post_comment_community.pk)
            blocked_users_query_staff_members.add(Q(reactor__communities_memberships__is_administrator=True) | Q(
                reactor__communities_memberships__is_moderator=True), Q.AND)

            blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
            reactions_query.add(blocked_users_query, Q.AND)
    else:
        blocked_users_query = ~Q(Q(reactor__blocked_by_users__blocker_id=self.pk) | Q(
            reactor__user_blocks__blocked_user_id=self.pk))
        reactions_query.add(blocked_users_query, Q.AND)

    if max_id:
        reactions_query.add(Q(id__lt=max_id), Q.AND)

    if emoji_id:
        reactions_query.add(Q(emoji_id=emoji_id), Q.AND)

    return reactions_query


def _make_get_post_comment_with_id_query(self, post_comment_id, item, post_comment_parent_id=None):

    post_comments_query = self._make_get_comments_for_post_query(item=item,
                                                                 post_comment_parent_id=post_comment_parent_id)

    post_comment_query = Q(pk=post_comment_id)
    post_comments_query.add(post_comment_query, Q.AND)
    return post_comments_query


def _make_get_comments_for_post_query(self, item, post_comment_parent_id=None, max_id=None, min_id=None):
    """ получаем комментарии записи с пристрастием """

    # список комментариев
    comments_query = Q(item_id=item.pk)

    # Если мы получаем ответы, добавьте parent_comment в запрос
    if post_comment_parent_id is None:
        comments_query.add(Q(parent_comment__isnull=True), Q.AND)
    else:
        comments_query.add(Q(parent_comment__id=post_comment_parent_id), Q.AND)

    post_community = item.community

    if post_community:
        if not self.is_staff_of_community_with_name(community_name=post_community.name):
            # Не извлекайте записи заблокированных пользователей, за исключением сотрудников
            blocked_users_query = ~Q(Q(commenter__blocked_by_users__blocker_id=self.pk) | Q(
                commenter__user_blocks__blocked_user_id=self.pk))
            blocked_users_query_staff_members = Q(
                commenter__communities_memberships__community_id=post_community.pk)
            blocked_users_query_staff_members.add(Q(commenter__communities_memberships__is_administrator=True) | Q(
                commenter__communities_memberships__is_moderator=True), Q.AND)

            blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
            comments_query.add(blocked_users_query, Q.AND)

            # Не извлекайте элементы, которые были зарегистрированы и утверждены
            comments_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)
    else:
        #  Не извлекайте сообщения заблокированных пользователей
        blocked_users_query = ~Q(Q(commenter__blocked_by_users__blocker_id=self.pk) | Q(
            commenter__user_blocks__blocked_user_id=self.pk))
        comments_query.add(blocked_users_query, Q.AND)

    # Запросы прокрутки на основе курсора
    if max_id:
        comments_query.add(Q(id__lt=max_id), Q.AND)
    elif min_id:
        comments_query.add(Q(id__gte=min_id), Q.AND)

    # Не извлекайте предметы, о которых получены репорты
    comments_query.add(~Q(moderated_object__reports__reporter_id=self.pk), Q.AND)
    # Не извлекайте мягко удаленные комментарии к сообщению
    comments_query.add(Q(is_deleted=False), Q.AND)
    return comments_query


def _make_get_community_with_id_posts_query(self, community, include_closed_posts_for_staff=True):
    """ получаем записи сообщества с пристрастием """

    # Извлечение записей сообщества
    community_posts_query = Q(community_id=community.pk, is_deleted=False, status=Item.STATUS_PUBLISHED)

    community_posts_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)

    # Не извлекайте предметы, о которых есть репорты
    community_posts_query.add(~Q(moderated_object__reports__reporter_id=self.pk), Q.AND)

    # Получаем записи, если они не запрещены
    community_posts_query.add(~Q(community__banned_users__id=self.pk), Q.AND)

    # Убедитесь, что публичная/частная видимость соблюдается
    community_posts_visibility_query = Q(community__memberships__user__id=self.pk)
    community_posts_visibility_query.add(Q(community__type=Community.COMMUNITY_TYPE_PUBLIC, ), Q.OR)

    community_posts_query.add(community_posts_visibility_query, Q.AND)

    if not self.is_staff_of_community_with_name(community_name=community.name):
        # Не извлекайте закрытые записи
        community_posts_query.add(Q(is_closed=False) | Q(creator_id=self.pk), Q.AND)

        # Не извлекайте записи заблокированных пользователей, за исключением тех случаев, когда они являются сотрудниками
        blocked_users_query = ~Q(Q(creator__blocked_by_users__blocker_id=self.pk) | Q(
        creator__user_blocks__blocked_user_id=self.pk))

        blocked_users_query_staff_members = Q(creator__communities_memberships__community_id=community)
        blocked_users_query_staff_members.add(Q(creator__communities_memberships__is_administrator=True) | Q(
        creator__communities_memberships__is_moderator=True), Q.AND)

        blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
        community_posts_query.add(blocked_users_query, Q.AND)
    else:
        if not include_closed_posts_for_staff:
            community_posts_query.add(Q(is_closed=False), Q.AND)
            return community_posts_query


def mute_post_with_id(self, item_id):
    item = Item.objects.get(pk=item_id)
    return self.mute_post(item=item)

def mute_post(self, post):
    check_can_mute_post(user=self, item=item)
    ItemMute.create_post_mute(item_id=item.pk, muter_id=self.pk)
    return item

def unmute_post_with_id(self, item_id):
    item = Item.objects.get(pk=item_id)

    check_can_unmute_post(user=self, item=item)
    self.item_mutes.filter(item_id=item_id).delete()
    return item

def mute_post_comment_with_id(self, post_comment_id):
    post_comment = ItemComment.objects.get(pk=post_comment_id)
    return self.mute_post_comment(post_comment=post_comment)

def mute_post_comment(self, post_comment):
    check_can_mute_post_comment(user=self, post_comment=post_comment)
    ItemCommentMute.create_post_comment_mute(post_comment_id=post_comment.pk, muter_id=self.pk)
    return post_comment

def unmute_post_comment_with_id(self, post_comment_id):
    post_comment = Item_comment.objects.get(pk=post_comment_id)

    check_can_unmute_post_comment(user=self, post_comment=post_comment)
    self.post_comment_mutes.filter(post_comment_id=post_comment_id).delete()
    return post_comment


def get_timeline_posts(self, lists_ids=None, circles_ids=None, max_id=None, min_id=None, count=None):
        """
        Get the timeline posts for self. The results will be dynamic based on follows and connections.
        """

        if not circles_ids and not lists_ids:
            return self._get_timeline_posts_with_no_filters(max_id=max_id, min_id=min_id, count=count)

        return self._get_timeline_posts_with_filters(max_id=max_id, circles_ids=circles_ids, lists_ids=lists_ids)

def _get_timeline_posts_with_no_filters(self, max_id=None, min_id=None, count=10):
    """
    получаем таймлайн записей
    """

    posts_select_related = ('creator', 'creator__profile', 'community', 'image')

    posts_only = ('text', 'id', 'uuid', 'created', 'image__image',
                  'creator__username', 'creator__id', 'creator__profile__name', 'creator__profile__avatar',
                  'creator__profile__id', 'community__id', 'community__name', 'community__avatar',
                  'community__title')

    reported_posts_exclusion_query = ~Q(moderated_object__reports__reporter_id=self.pk)

    own_posts_query = Q(creator=self.pk, community__isnull=True, is_deleted=False, status=Item.STATUS_PUBLISHED)

    own_posts_query.add(reported_posts_exclusion_query, Q.AND)

    if max_id:
        own_posts_query.add(Q(id__lt=max_id), Q.AND)

    own_posts_queryset = self.posts.select_related(*posts_select_related).prefetch_related(
        *posts_prefetch_related).only(*posts_only).filter(own_posts_query)

    community_posts_query = Q(community__memberships__user__id=self.pk, is_closed=False, is_deleted=False,
                              status=Item.STATUS_PUBLISHED)

    community_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=self.pk) | Q(
        creator__user_blocks__blocked_user_id=self.pk)), Q.AND)

    if max_id:
        community_posts_query.add(Q(id__lt=max_id), Q.AND)

    community_posts_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)

    community_posts_query.add(reported_posts_exclusion_query, Q.AND)

    community_posts_queryset = Item.objects.select_related(*posts_select_related).prefetch_related(
        *posts_prefetch_related).only(*posts_only).filter(community_posts_query)

    followed_users = self.follows.values('followed_user_id')

    followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]

    followed_users_query = Q(creator__in=followed_users_ids, is_deleted=False, status=Post.STATUS_PUBLISHED)

    followed_users_query.add(reported_posts_exclusion_query, Q.AND)

    if max_id:
        followed_users_query.add(Q(id__lt=max_id), Q.AND)

    followed_users_queryset = Item.objects.select_related(*posts_select_related).prefetch_related(
        *posts_prefetch_related).only(*posts_only).filter(followed_users_query)

    final_queryset = own_posts_queryset.union(community_posts_queryset, followed_users_queryset)

    return final_queryset

    def _get_timeline_posts_with_filters(self, max_id=None, min_id=None):

        timeline_posts_query = Q()

        if lists_ids:
            followed_users_query = self.follows.filter(lists__id__in=lists_ids)
        else:
            followed_users_query = self.follows.all()

        followed_users = followed_users_query.values('followed_user__id').cache()

        for followed_user in followed_users:

            followed_user_id = followed_user['followed_user__id']

            followed_user_query = Q(creator_id=followed_user_id)

            if circles_ids:
                followed_user_query.add(Q(creator__connections__target_connection__circles__in=circles_ids), Q.AND)

            followed_user_query.add(followed_user_circles_query, Q.AND)

            timeline_posts_query.add(followed_user_query, Q.OR)

        if max_id:
            timeline_posts_query.add(Q(id__lt=max_id), Q.AND)
        elif min_id:
            timeline_posts_query.add(Q(id__gt=min_id), Q.AND)

        timeline_posts_query.add(Q(is_deleted=False, status=Post.STATUS_PUBLISHED), Q.AND)

        timeline_posts_query.add(~Q(moderated_object__reports__reporter_id=self.pk), Q.AND)

        return Item.objects.filter(timeline_posts_query).distinct()


def get_post_with_id(self, item_id):
    item = Item.objects.get(pk=item_id)
    check_can_see_post(user=self, item=item)
    return item


  def open_post_with_id(self, item_id):
    check_can_open_post_with_id(user=self, item_id=item_id)
    item = Item.objects.select_related('community').get(id=post_id)
    item.community.create_open_post_log(source_user=self, target_user=post.creator, item=item)
    item.is_closed = False
    item.save()

    return post

def close_post_with_id(self, item_id):
    item = Item.objects.select_related('community').get(id=item_id)
    return self.close_post(item=item)

def close_post(self, post):
    check_can_close_post(user=self, item=item)
    item.community.create_close_post_log(source_user=self, target_user=item.creator, item=item)
    item.is_closed = True
    item.save()

    return item



def get_media_for_post_with_uuid(self, item_uuid):
    item = Item.objects.get(uuid=item_uuid)
    return self.get_media_for_post(item=item)

def get_media_for_post(self, item):
    check_can_get_media_for_post(user=self, item=item)
    return item.get_media()

def add_media_to_post_with_uuid(self, file, item_uuid, order):
    item = Item.objects.get(uuid=item_uuid)
    return self.add_media_to_post(item=item, file=file, order=order)

def add_media_to_post(self, file, item, order=None):
    check_can_add_media_to_post(user=self, item=item)
    item.add_media(file=file, order=order)
    return item

def publish_post_with_uuid(self, item_uuid):
    item = Item.objects.get(uuid=item_uuid)
    return self.publish_post(item=item)

def delete_post_with_uuid(self, item_uuid):
    item = Item.objects.get(uuid=post_uuid)
    return self.delete_post(item=item)

def delete_post(self, item):
    check_can_delete_post(user=self, item=item)
    # Этот метод переопределен
    item.delete()

def get_trending_posts(self):
    return Item.get_trending_posts_for_user_with_id(user_id=self.pk)


def react_to_post_with_id(self, item_id, emoji_id):
    item = Post.objects.get(pk=item_id)
    return self.react_to_post(item=item, emoji_id=emoji_id)

def react_to_post(self, item, emoji_id):
    check_can_react_to_post(user=self, item=item)
    check_can_react_with_emoji_id(user=self, emoji_id=emoji_id)

    item_id = item.pk

    if self.has_reacted_to_post_with_id(item_id):
        post_reaction = self.post_reactions.get(item_id=item_id)
        post_reaction.emoji_id = emoji_id
        post_reaction.save()
    else:
        post_reaction = item.react(reactor=self, emoji_id=emoji_id)
        if post_reaction.item.creator_id != self.pk:
            if item.creator.has_reaction_notifications_enabled_for_post_with_id(item_id=item.pk) and \
                    not item.creator.has_blocked_user_with_id(self.pk):
                self._create_post_reaction_notification(post_reaction=post_reaction)
            self._send_post_reaction_push_notification(post_reaction=post_reaction)

    return post_reaction


def delete_reaction_with_id_for_post_with_id(self, post_reaction_id, item_id):
    item = Item.objects.get(pk=item_id)
    check_can_delete_reaction_with_id_for_post(user=self, post_reaction_id=post_reaction_id, item=item)
    post_reaction = PostReaction.objects.filter(pk=post_reaction_id).get()
    self._delete_post_reaction_notification(post_reaction=post_reaction)
    post_reaction.delete()

def react_to_post_comment_with_id(self, post_comment_id, emoji_id):
    post_comment = PostComment.objects.get(pk=post_comment_id)
    return self.react_to_post_comment(post_comment=post_comment, emoji_id=emoji_id)

def react_to_post_comment(self, post_comment, emoji_id):
    check_can_react_to_post_comment(user=self, post_comment=post_comment, emoji_id=emoji_id)

    post_comment_id = post_comment.pk

    if self.has_reacted_to_post_comment_with_id(post_comment_id):
        post_comment_reaction = self.post_comment_reactions.get(post_comment_id=post_comment_id)
        post_comment_reaction.emoji_id = emoji_id
        post_comment_reaction.save()
    else:
        post_comment_reaction = post_comment.react(reactor=self, emoji_id=emoji_id)
        if post_comment_reaction.post_comment.commenter_id != self.pk:
            commenter_has_reaction_notifications_enabled = post_comment.commenter.has_reaction_notifications_enabled_for_post_comment(
                post_comment=post_comment)

            if commenter_has_reaction_notifications_enabled:
                self._send_post_comment_reaction_push_notification(post_comment_reaction=post_comment_reaction)
            self._create_post_comment_reaction_notification(post_comment_reaction=post_comment_reaction)

    return post_comment_reaction

def delete_post_comment_reaction_with_id(self, post_comment_reaction_id):
    post_comment_reaction = PostCommentReaction.objects.filter(pk=post_comment_reaction_id).get()
    return self.delete_post_comment_reaction(post_comment_reaction=post_comment_reaction)

def delete_post_comment_reaction(self, post_comment_reaction):
    check_can_delete_post_comment_reaction(user=self, post_comment_reaction=post_comment_reaction)
    self._delete_post_comment_reaction_notification(post_comment_reaction=post_comment_reaction)
    post_comment_reaction.delete()

def get_comments_for_post_with_id(self, item_id, min_id=None, max_id=None):
    item = Item.objects.get(pk=item_id)

    check_can_get_comments_for_post(user=self, item=item)

    comments_query = self._make_get_comments_for_post_query(item=item, max_id=max_id, min_id=min_id)
    return PostComment.objects.filter(comments_query)

def get_comment_replies_for_comment_with_id_with_post_with_uuid(self, post_comment_id, item_uuid, min_id=None,
                                                                max_id=None):

    post_comment = PostComment.objects.get(pk=post_comment_id)
    item = Item.objects.get(uuid=item_uuid)
    return self.get_comment_replies_for_comment_with_post(item=item, post_comment=post_comment, min_id=min_id,
                                                              max_id=max_id)

def get_comment_replies_for_comment_with_post(self, item, post_comment, min_id=None, max_id=None):
    check_can_get_comment_replies_for_post_and_comment(user=self, item=item, post_comment=post_comment)

    comment_replies_query = self._make_get_comments_for_post_query(item=item,
                                                                   post_comment_parent_id=post_comment.pk,
                                                                   max_id=max_id,
                                                                   min_id=min_id)

    return PostComment.objects.filter(comment_replies_query)

def get_comments_count_for_post(self, item):
    return item.count_comments_with_user(user=self)

def get_replies_count_for_post_comment(self, post_comment):
    return post_comment.count_replies_with_user(user=self)

def get_status_for_post_with_uuid(self, item_uuid):

    item = Item.objects.get(uuid=item_uuid)
    return self.get_status_for_post(item=item)

def get_status_for_post(self, item):
    check_can_get_status_for_post(user=self, item=item)
    return item.status


def can_see_post_comment(self, post_comment):
    item = post_comment.post
    if not self.can_see_post(item=item):
        return False
    post_comment_query = self._make_get_post_comment_with_id_query(post_comment_id=post_comment.pk,
                                                                   post_comment_parent_id=post_comment.parent_comment_id,
                                                                   item=item)

    return PostComment.objects.filter(post_comment_query).exists()


def get_reaction_for_post_with_id(self, item_id):
    return self.post_reactions.filter(item_id=item_id).get()

def get_reactions_for_post_with_id(self, item_id, max_id=None, emoji_id=None):
    item = Item.objects.get(pk=post_id)

    return self.get_reactions_for_post(item=item, max_id=max_id, emoji_id=emoji_id)

def get_reactions_for_post(self, item, max_id=None, emoji_id=None):
    check_can_get_reactions_for_post(user=self, item=item)

    reactions_query = self._make_get_reactions_for_post_query(item=item, emoji_id=emoji_id, max_id=max_id)
    return PostReaction.objects.filter(reactions_query)

def get_emoji_counts_for_post_with_id(self, item_id, emoji_id=None):
    item = Item.objects.select_related('community').get(pk=item_id)
    return self.get_emoji_counts_for_post(item=item, emoji_id=emoji_id)

def get_emoji_counts_for_post(self, item, emoji_id=None):
    check_can_get_reactions_for_post(user=self, item=item)

    emoji_query = Q(post_reactions__item_id=item.pk, )

    if emoji_id:
        emoji_query.add(Q(post_reactions__emoji_id=emoji_id), Q.AND)

    post_community = item.community

    if post_community:
        if not self.is_staff_of_community_with_name(community_name=post_community.name)
            blocked_users_query = ~Q(Q(post_reactions__reactor__blocked_by_users__blocker_id=self.pk) | Q(
                post_reactions__reactor__user_blocks__blocked_user_id=self.pk))
            blocked_users_query_staff_members = Q(
                post_reactions__reactor__communities_memberships__community_id=post_community.pk)
            blocked_users_query_staff_members.add(
                Q(post_reactions__reactor__communities_memberships__is_administrator=True) | Q(
                    post_reactions__reactor__communities_memberships__is_moderator=True), Q.AND)

            blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
            emoji_query.add(blocked_users_query, Q.AND)
    else:
        # Show all, even blocked users reactions
        blocked_users_query = ~Q(Q(post_reactions__reactor__blocked_by_users__blocker_id=self.pk) | Q(
            post_reactions__reactor__user_blocks__blocked_user_id=self.pk))
        emoji_query.add(blocked_users_query, Q.AND)

    emojis = Emoji.objects.filter(emoji_query).annotate(Count('post_reactions')).distinct().order_by(
        '-post_reactions__count').cache().all()

    return [{'emoji': emoji, 'count': emoji.post_reactions__count} for emoji in emojis]

def get_emoji_counts_for_post_comment_with_id(self, post_comment_id, emoji_id=None):
    post_comment = PostComment.objects.get(pk=post_comment_id)
    return self.get_emoji_counts_for_post_comment(post_comment=post_comment, emoji_id=emoji_id)

def get_emoji_counts_for_post_comment(self, post_comment, emoji_id=None):
    check_can_get_reactions_for_post_comment(user=self, post_comment=post_comment)

    emoji_query = Q(post_comment_reactions__post_comment_id=post_comment.pk, )

    if emoji_id:
        emoji_query.add(Q(post_comment_reactions__emoji_id=emoji_id), Q.AND)

    post_comment_community = post_comment.post.community

    if post_comment_community:
        if not self.is_staff_of_community_with_name(community_name=post_comment_community.name):
            # Exclude blocked users reactions
            blocked_users_query = ~Q(Q(post_comment_reactions__reactor__blocked_by_users__blocker_id=self.pk) | Q(
                post_comment_reactions__reactor__user_blocks__blocked_user_id=self.pk))
            blocked_users_query_staff_members = Q(
                post_comment_reactions__reactor__communities_memberships__community_id=post_comment_community.pk)
            blocked_users_query_staff_members.add(
                Q(post_comment_reactions__reactor__communities_memberships__is_administrator=True) | Q(
                    post_comment_reactions__reactor__communities_memberships__is_moderator=True), Q.AND)

            blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
            emoji_query.add(blocked_users_query, Q.AND)
    else:
        # Show all, even blocked users reactions
        blocked_users_query = ~Q(Q(post_comment_reactions__reactor__blocked_by_users__blocker_id=self.pk) | Q(
            post_comment_reactions__reactor__user_blocks__blocked_user_id=self.pk))
        emoji_query.add(blocked_users_query, Q.AND)

    emojis = Emoji.objects.filter(emoji_query).annotate(Count('post_comment_reactions')).distinct().order_by(
        '-post_comment_reactions__count').cache().all()

    return [{'emoji': emoji, 'count': emoji.post_comment_reactions__count} for emoji in emojis]

def get_reaction_for_post_comment_with_id(self, post_comment_id):
    return self.post_comment_reactions.filter(post_comment_id=post_comment_id).get()

def get_reactions_for_post_comment_with_id(self, post_comment_id, max_id=None, emoji_id=None):
    post_comment = Post_comment.objects.get(pk=post_comment_id)

    return self.get_reactions_for_post_comment(post_comment=post_comment, max_id=max_id, emoji_id=emoji_id)

def get_reactions_for_post_comment(self, post_comment, max_id=None, emoji_id=None):
    check_can_get_reactions_for_post_comment(user=self, post_comment=post_comment)

    reactions_query = self._make_get_reactions_for_post_comment_query(post_comment=post_comment,
                                                                      emoji_id=emoji_id, max_id=max_id)

    return PostCommentReaction.objects.filter(reactions_query)

    def react_to_post_with_id(self, item_id, emoji_id):
        item = Item.objects.get(pk=post_id)
        return self.react_to_post(item=item, emoji_id=emoji_id)

def react_to_post(self, item, emoji_id):
    check_can_react_to_post(user=self, item=item)
    check_can_react_with_emoji_id(user=self, emoji_id=emoji_id)

    item_id = item.pk

    if self.has_reacted_to_post_with_id(item_id):
        post_reaction = self.post_reactions.get(item_id=ite_id)
        post_reaction.emoji_id = emoji_id
        post_reaction.save()
    else:
        post_reaction = item.react(reactor=self, emoji_id=emoji_id)
        if post_reaction.post.creator_id != self.pk:
            if item.creator.has_reaction_notifications_enabled_for_post_with_id(item_id=item.pk) and \
                    not item.creator.has_blocked_user_with_id(self.pk):
                self._create_post_reaction_notification(post_reaction=post_reaction)
            self._send_post_reaction_push_notification(post_reaction=post_reaction)

    return post_reaction

def delete_reaction_with_id_for_post_with_id(self, post_reaction_id, item_id):
    item = Item.objects.get(pk=item_id)
    check_can_delete_reaction_with_id_for_post(user=self, post_reaction_id=post_reaction_id, item=item)
    post_reaction = PostReaction.objects.filter(pk=post_reaction_id).get()
    self._delete_post_reaction_notification(post_reaction=post_reaction)
    post_reaction.delete()

def react_to_post_comment_with_id(self, post_comment_id, emoji_id):
    post_comment = PostComment.objects.get(pk=post_comment_id)
    return self.react_to_post_comment(post_comment=post_comment, emoji_id=emoji_id)

def react_to_post_comment(self, post_comment, emoji_id):
    check_can_react_to_post_comment(user=self, post_comment=post_comment, emoji_id=emoji_id)

    post_comment_id = post_comment.pk

    if self.has_reacted_to_post_comment_with_id(post_comment_id):
        post_comment_reaction = self.post_comment_reactions.get(post_comment_id=post_comment_id)
        post_comment_reaction.emoji_id = emoji_id
        post_comment_reaction.save()
    else:
        post_comment_reaction = post_comment.react(reactor=self, emoji_id=emoji_id)
        if post_comment_reaction.post_comment.commenter_id != self.pk:
            commenter_has_reaction_notifications_enabled = post_comment.commenter.has_reaction_notifications_enabled_for_post_comment(
                post_comment=post_comment)

            if commenter_has_reaction_notifications_enabled:
                self._send_post_comment_reaction_push_notification(post_comment_reaction=post_comment_reaction)
            self._create_post_comment_reaction_notification(post_comment_reaction=post_comment_reaction)

    return post_comment_reaction

def delete_post_comment_reaction_with_id(self, post_comment_reaction_id):
    post_comment_reaction = PostCommentReaction.objects.filter(pk=post_comment_reaction_id).get()
    return self.delete_post_comment_reaction(post_comment_reaction=post_comment_reaction)

def delete_post_comment_reaction(self, post_comment_reaction):
    check_can_delete_post_comment_reaction(user=self, post_comment_reaction=post_comment_reaction)
    self._delete_post_comment_reaction_notification(post_comment_reaction=post_comment_reaction)
    post_comment_reaction.delete()

def get_comments_for_post_with_id(self, item_id, min_id=None, max_id=None):

    item = Item.objects.get(pk=item_id)

    check_can_get_comments_for_post(user=self, item=item)

    comments_query = self._make_get_comments_for_post_query(item=item, max_id=max_id, min_id=min_id)
    return PostComment.objects.filter(comments_query)

def get_comment_replies_for_comment_with_id_with_post_with_uuid(self, post_comment_id, item_uuid, min_id=None,
                                                                max_id=None):

    post_comment = PostComment.objects.get(pk=post_comment_id)
    item = Item.objects.get(uuid=item_uuid)
    return self.get_comment_replies_for_comment_with_post(item=item, post_comment=post_comment, min_id=min_id,
                                                          max_id=max_id)

def get_comment_replies_for_comment_with_post(self, item, post_comment, min_id=None, max_id=None):
    check_can_get_comment_replies_for_post_and_comment(user=self, item=item, post_comment=post_comment)

    comment_replies_query = self._make_get_comments_for_post_query(item=item,
                                                                   post_comment_parent_id=post_comment.pk,
                                                                   max_id=max_id,
                                                                   min_id=min_id)

    return PostComment.objects.filter(comment_replies_query)

def get_comments_count_for_post(self, item):
    return item.count_comments_with_user(user=self)

def get_replies_count_for_post_comment(self, post_comment):
    return post_comment.count_replies_with_user(user=self)

def get_status_for_post_with_uuid(self, item_uuid):
    item = Item.objects.get(uuid=item_uuid)
    return self.get_status_for_post(item=item)


def can_see_post(self, item):
    if item.community:
        if self._can_see_community_post(community=post.community, item=item):
            return True
    elif item.creator_id == self.pk and not item.is_deleted:
        return True
    else:
        # Check if we can retrieve the post
        if self._can_see_post(item=item):
            return True

    return False


def has_reacted_to_post_with_id(self, item_id, emoji_id=None):
    has_reacted_query = Q(item_id=item_id)

    if emoji_id:
        has_reacted_query.add(Q(emoji_id=emoji_id), Q.AND)

    return self.post_reactions.filter(has_reacted_query).exists()

def has_reacted_to_post_comment_with_id(self, post_comment_id, emoji_id=None):
    has_reacted_query = Q(post_comment_id=post_comment_id)

    if emoji_id:
        has_reacted_query.add(Q(emoji_id=emoji_id), Q.AND)

    return self.post_comment_reactions.filter(has_reacted_query).exists()

def has_commented_post_with_id(self, item_id):
    return self.posts_comments.filter(item_id=item_id).exists()
