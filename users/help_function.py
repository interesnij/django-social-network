from posts.models import Item
from moderation.models import ModeratedObject
from communities.models import Community


def _can_see_post(self, item):
        post_query = self._make_get_post_with_id_query_for_user(item.creator, item_id=item.pk)
        profile_posts = Item.objects.filter(post_query)
        return profile_posts.exists()


def _can_see_community_post(self, community, item):
        if item.creator_id == self.pk:
            return True

        community_posts_query = self._make_get_community_with_id_posts_query(community=community)
        community_posts_query.add(Q(pk=item.pk), Q.AND)
        return Item.objects.filter(community_posts_query).exists()


def _make_get_reactions_for_post_query(self, item, max_id=None, emoji_id=None):
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
    """ получаем записи сообщения записи с пристрастием """

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
                # Не извлекайте сообщения заблокированных пользователей, за исключением сотрудников
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

        # Не извлекайте элементы, которые были зарегистрированы и утверждены
        ModeratedObject = get_moderated_object_model()
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
