from django.db.models import Q
from posts.models import Post


def get_timeline_posts_for_user(user):
    own_posts_query = Q(creator_id=user.pk, community__isnull=True, is_deleted=False, status=Post.STATUS_PUBLISHED)
    own_posts_queryset = user.post_creator.only('created').filter(own_posts_query)

    community_posts_query = Q(community__memberships__user__id=user.pk, is_deleted=False, status=Post.STATUS_PUBLISHED)
    community_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_posts_queryset = Post.objects.only('created').filter(community_posts_query)

    followed_users = user.follows.values('followed_user_id')
    followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]
    followed_users_query = Q(creator__in=followed_users_ids, creator__user_private__is_private=False, is_deleted=False, status=Post.STATUS_PUBLISHED)
    followed_users_queryset = Post.objects.only('created').filter(followed_users_query)

    frends = user.connections.values('target_user_id')
    frends_ids = [target_user['target_user_id'] for target_user in frends]
    frends_query = Q(creator__in=frends_ids, is_deleted=False, status=Post.STATUS_PUBLISHED)
    frends_queryset = Post.objects.only('created').filter(frends_query)
    final_queryset = own_posts_queryset.union(community_posts_queryset, followed_users_queryset, frends_queryset)
    return final_queryset

def get_timeline_posts_for_possible_users(user):
    possible_users = user.get_possible_friends_ids()
    posts_query = Q(creator_id__in=possible_users, community__isnull=True, is_deleted=False, status=Post.STATUS_PUBLISHED)
    posts_queryset = Post.objects.only('created').filter(posts_query)
    community_query = Q(community__memberships__user__id__in=possible_users, is_deleted=False, status=Post.STATUS_PUBLISHED)
    community_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_queryset = Post.objects.only('created').filter(community_query)
    final_queryset = posts_queryset.union(community_queryset)
    return final_queryset
