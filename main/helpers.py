from django.http import HttpResponseBadRequest


def ajax_required(f):
    """Не миксин, но хороший декоратор для проверки, чем запрос является AJAX"""
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def _make_get_comments_for_post_query(item, user_id, post_comment_parent_id=None):
    """ получаем комментарии записи с пристрастием """
    comments_query = Q(item_id=item.pk)

    if post_comment_parent_id is None:
        comments_query.add(Q(parent_comment__isnull=True), Q.AND)
    else:
        comments_query.add(Q(parent_comment__id=post_comment_parent_id), Q.AND)

    post_community = item.community

    if post_community:
        if not self.is_staff_of_community_with_name(community_name=post_community.name):
            blocked_users_query = ~Q(Q(commenter__blocked_by_users__blocker_id=user_id) | Q(
                commenter__user_blocks__blocked_user_id=user_id))
            blocked_users_query_staff_members = Q(
                commenter__communities_memberships__community_id=post_community.pk)
            blocked_users_query_staff_members.add(Q(commenter__communities_memberships__is_administrator=True) | Q(
                commenter__communities_memberships__is_moderator=True), Q.AND)
            blocked_users_query.add(~blocked_users_query_staff_members, Q.AND)
            comments_query.add(blocked_users_query, Q.AND)
            comments_query.add(~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED), Q.AND)
    else:
        blocked_users_query = ~Q(Q(commenter__blocked_by_users__blocker_id=user_id) | Q(
            commenter__user_blocks__blocked_user_id=user_id))
        comments_query.add(blocked_users_query, Q.AND)

    comments_query.add(~Q(moderated_object__reports__reporter_id=user_id), Q.AND)
    comments_query.add(Q(is_deleted=False), Q.AND)
    return comments_query
