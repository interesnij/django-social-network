from posts.models import Post
from moderation.models import ModeratedObject
from communities.models import Community


def _make_get_community_with_id_posts_query(self, community, include_closed_posts_for_staff=True):
    """ получаем записи сообщества с пристрастием """

        # Извлечение записей сообщества
        community_posts_query = Q(community_id=community.pk, is_deleted=False, status=Post.STATUS_PUBLISHED)

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


def _make_get_comments_for_post_query(self, post, post_comment_parent_id=None, max_id=None, min_id=None):
    """ получаем записи сообщения записи с пристрастием """

        # список комментариев
        comments_query = Q(post_id=post.pk)

        # Если мы получаем ответы, добавьте parent_comment в запрос
        if post_comment_parent_id is None:
            comments_query.add(Q(parent_comment__isnull=True), Q.AND)
        else:
            comments_query.add(Q(parent_comment__id=post_comment_parent_id), Q.AND)

        post_community = post.community

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
