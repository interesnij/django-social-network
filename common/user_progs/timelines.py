from django.db.models import Q
from posts.models import Post
from gallery.models import Photo
from goods.models import Good
from video.models import VideoAlbum
from music.models import SoundList


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
    final_queryset = own_posts_queryset.union(community_posts_queryset, followed_users_queryset, frends_queryset).order_by("-created")
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


def get_timeline_photos_for_user(user):
    own_photos_query = Q(creator_id=user.pk, community__isnull=True, is_deleted=False, is_public=True)
    own_photos_queryset = user.photo_creator.only('created').filter(own_photos_query)

    community_photos_query = Q(community__memberships__user__id=user.pk, is_deleted=False, is_public=True)
    community_photos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_photos_queryset = Photo.objects.only('created').filter(community_photos_query)

    followed_users = user.follows.values('followed_user_id')
    followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]
    followed_users_query = Q(creator__in=followed_users_ids, creator__user_private__is_private=False, is_deleted=False, is_public=True)
    followed_users_queryset = Photo.objects.only('created').filter(followed_users_query)

    frends = user.connections.values('target_user_id')
    frends_ids = [target_user['target_user_id'] for target_user in frends]
    frends_query = Q(creator__in=frends_ids, is_deleted=False, is_public=True)
    frends_queryset = Photo.objects.only('created').filter(frends_query)
    final_queryset = own_photos_queryset.union(community_photos_queryset, followed_users_queryset, frends_queryset)
    return final_queryset

def get_timeline_photos_for_possible_users(user):
    possible_users = user.get_possible_friends_ids()
    photos_query = Q(creator_id__in=possible_users, community__isnull=True, is_deleted=False, is_public=True)
    photos_queryset = Photo.objects.only('created').filter(photos_query)
    community_query = Q(community__memberships__user__id__in=possible_users, is_deleted=False, is_public=True)
    community_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_queryset = Photo.objects.only('created').filter(community_query)
    final_queryset = photos_queryset.union(community_queryset)
    return final_queryset


def get_timeline_goods_for_user(user):
    own_goods_query = Q(creator_id=user.pk, community__isnull=True, is_deleted=False, status=Good.STATUS_PUBLISHED)
    own_goods_queryset = user.good_creator.only('created').filter(own_goods_query)

    community_goods_query = Q(community__memberships__user__id=user.pk, is_deleted=False, status=Good.STATUS_PUBLISHED)
    community_goods_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_goods_queryset = Good.objects.only('created').filter(community_goods_query)

    followed_users = user.follows.values('followed_user_id')
    followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]
    followed_users_query = Q(creator__in=followed_users_ids, creator__user_private__is_private=False, is_deleted=False, status=Good.STATUS_PUBLISHED)
    followed_users_queryset = Good.objects.only('created').filter(followed_users_query)

    frends = user.connections.values('target_user_id')
    frends_ids = [target_user['target_user_id'] for target_user in frends]
    frends_query = Q(creator__in=frends_ids, is_deleted=False, status=Good.STATUS_PUBLISHED)
    frends_queryset = Good.objects.only('created').filter(frends_query)
    final_queryset = own_goods_queryset.union(community_goods_queryset, followed_users_queryset, frends_queryset)
    return final_queryset

def get_timeline_goods_for_possible_users(user):
    possible_users = user.get_possible_friends_ids()
    goods_query = Q(creator_id__in=possible_users, community__isnull=True, is_deleted=False, status=Good.STATUS_PUBLISHED)
    goods_queryset = Good.objects.only('created').filter(goods_query)
    community_query = Q(community__memberships__user__id__in=possible_users, is_deleted=False, status=Good.STATUS_PUBLISHED)
    community_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_queryset = Good.objects.only('created').filter(community_query)
    final_queryset = goods_queryset.union(community_queryset)
    return final_queryset


def get_timeline_videos_for_user(user):
    empty_list_exclude = Q(video_album__isnull=True)
    own_videos_query = Q(creator_id=user.pk, community__isnull=True, is_deleted=False, is_public=True)
    own_videos_query.add(~Q(empty_list_exclude), Q.AND)
    own_videos_queryset = user.video_user_creator.only('id').filter(own_videos_query)

    community_videos_query = Q(community__memberships__user__id=user.pk, is_deleted=False, is_public=True)
    community_videos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_videos_query.add(~Q(empty_list_exclude), Q.AND)
    community_videos_queryset = VideoAlbum.objects.only('id').filter(community_videos_query)

    followed_users = user.follows.values('followed_user_id')
    followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]
    followed_users_query = Q(creator__in=followed_users_ids, creator__user_private__is_private=False, is_deleted=False, is_public=True)
    followed_users_query.add(~Q(empty_list_exclude), Q.AND)
    followed_users_queryset = VideoAlbum.objects.only('id').filter(followed_users_query)

    frends = user.connections.values('target_user_id')
    frends_ids = [target_user['target_user_id'] for target_user in frends]
    frends_query = Q(creator__in=frends_ids, is_deleted=False, is_public=True)
    frends_query.add(~Q(empty_list_exclude), Q.AND)
    frends_queryset = VideoAlbum.objects.only('id').filter(frends_query)
    final_queryset = own_videos_queryset.union(community_videos_queryset, followed_users_queryset, frends_queryset)
    return final_queryset

def get_timeline_videos_for_possible_users(user):
    possible_users = user.get_possible_friends_ids()
    empty_list_exclude = Q(video_album__isnull=True)
    videos_query = Q(creator_id__in=possible_users, community__isnull=True, is_deleted=False, is_public=True)
    videos_query.add(~Q(empty_list_exclude), Q.AND)
    videos_queryset = VideoAlbum.objects.only('id').filter(videos_query)
    community_query = Q(community__memberships__user__id__in=possible_users, is_deleted=False, is_public=True)
    community_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_query.add(~Q(empty_list_exclude), Q.AND)
    community_queryset = VideoAlbum.objects.only('id').filter(community_query)
    final_queryset = videos_queryset.union(community_queryset)
    return final_queryset


def get_timeline_audios_for_user(user):
    empty_list_exclude = Q(players__isnull=True)
    own_audios_query = Q(creator_id=user.pk, community__isnull=True, is_deleted=False)
    own_audios_query.add(~Q(empty_list_exclude), Q.AND)
    own_audios_queryset = user.user_playlist.only('id').filter(own_audios_query)

    community_audios_query = Q(community__memberships__user__id=user.pk, is_deleted=False)
    community_audios_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_audios_query.add(~Q(empty_list_exclude), Q.AND)
    community_audios_queryset = SoundList.objects.only('id').filter(community_audios_query)

    followed_users = user.follows.values('followed_user_id')
    followed_users_ids = [followed_user['followed_user_id'] for followed_user in followed_users]
    followed_users_query = Q(creator__in=followed_users_ids, creator__user_private__is_private=False, is_deleted=False)
    followed_users_query.add(~Q(empty_list_exclude), Q.AND)
    followed_users_queryset = SoundList.objects.only('id').filter(followed_users_query)

    frends = user.connections.values('target_user_id')
    frends_ids = [target_user['target_user_id'] for target_user in frends]
    frends_query = Q(creator__in=frends_ids, is_deleted=False)
    frends_query.add(~Q(empty_list_exclude), Q.AND)
    frends_queryset = SoundList.objects.only('id').filter(frends_query)
    final_queryset = own_audios_queryset.union(community_audios_queryset, followed_users_queryset, frends_queryset)
    return final_queryset

def get_timeline_audios_for_possible_users(user):
    possible_users = user.get_possible_friends_ids()
    empty_list_exclude = Q(players__isnull=True)
    audios_query = Q(creator_id__in=possible_users, community__isnull=True, is_deleted=False)
    audios_query.add(~Q(empty_list_exclude), Q.AND)
    audios_queryset = SoundList.objects.only('id').filter(audios_query)
    community_query = Q(community__memberships__user__id__in=possible_users, is_deleted=False)
    community_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    community_query.add(~Q(empty_list_exclude), Q.AND)
    community_queryset = SoundList.objects.only('id').filter(community_query)
    final_queryset = audios_queryset.union(community_queryset)
    return final_queryset
