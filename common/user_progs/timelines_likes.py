from django.db.models import Q
from common.model.votes import PostVotes, PhotoVotes, GoodVotes, VideoVotes


def get_timeline_post_likes(user_pk):
    """ лента записей, которые понравились пользователю """
    from posts.models import Post

    likes = PostVotes.objects.filter(user_id=user_pk, vote=PostVotes.LIKE).values("parent_id")
    posts_ids = [post['parent_id'] for post in likes]
    own_posts_query = Q(id__in=posts_ids, is_deleted=False, status="P")
    own_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user_pk) | Q(creator__user_blocks__blocked_user_id=user_pk)), Q.AND)
    return Post.objects.only('pk').filter(own_posts_query)

def get_timeline_photo_likes(user_pk):
    """ лента фотоальбомов с последними фотографиями, которые понравились пользователю """
    from gallery.models import Photo

    likes = PhotoVotes.objects.filter(user_id=user_pk, vote=PhotoVotes.LIKE).values("parent_id")
    photos_ids = [photo['parent_id'] for photo in likes]
    own_photos_query = Q(id__in=photos_ids, is_deleted=False, is_public=True)
    own_photos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user_pk) | Q(creator__user_blocks__blocked_user_id=user_pk)), Q.AND)
    return Photo.objects.only('pk').filter(own_photos_query)

def get_timeline_good_likes(user_pk):
    """ лента товаров, которые понравились пользователю """
    from goods.models import Good

    likes = GoodVotes.objects.filter(user_id=user_pk, vote=GoodVotes.LIKE).values("parent_id")
    goods_ids = [good['parent_id'] for good in likes]
    own_goods_query = Q(id__in=goods_ids, is_deleted=False, status="P")
    own_goods_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user_pk) | Q(creator__user_blocks__blocked_user_id=user_pk)), Q.AND)
    return Good.objects.only('pk').filter(own_goods_query)

def get_timeline_video_likes(user_pk):
    """ лента видеоальбомов с последними роликами, которые понравились пользователю """
    from video.models import Video

    likes = VideoVotes.objects.filter(user_id=user_pk, vote=VideoVotes.LIKE).values("parent_id")
    videos_ids = [video['parent_id'] for video in likes]
    own_videos_query = Q(id__in=videos_ids, is_deleted=False, is_public=True)
    own_videos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user_pk) | Q(creator__user_blocks__blocked_user_id=user_pk)), Q.AND)
    return Video.objects.only('pk').filter(own_videos_query)


def get_timeline_featured_post_likes(user):
    """ лента записей, которые понравились друзьям пользователя и тем, на кого он подписан """
    possible_users = user.get_friends_and_followings_ids()
    likes = PostVotes.objects.filter(user_id__in=possible_users, vote=PostVotes.LIKE).values("parent_id")
    posts_ids = [post['parent_id'] for post in likes]
    own_posts_query = Q(id__in=posts_ids, is_deleted=False, status=Post.STATUS_PUBLISHED)
    own_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.post_creator.only('pk').filter(own_posts_query)

def get_timeline_featured_photo_likes(user):
    """ лента фотографий, которые понравились друзьям пользователя и тем, на кого он подписан """
    possible_users = user.get_friends_and_followings_ids()
    likes = PhotoVotes.objects.filter(user_id__in=possible_users, vote=PhotoVotes.LIKE).values("parent_id")
    photos_ids = [photo['parent_id'] for photo in likes]
    own_photos_query = Q(id__in=photos_ids, is_deleted=False, is_public=True)
    own_photos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.photo_creator.only('pk').filter(own_photos_query)

def get_timeline_featured_good_likes(user):
    """ лента товаров, которые понравились друзьям пользователя и тем, на кого он подписан """
    possible_users = user.get_friends_and_followings_ids()
    likes = GoodVotes.objects.filter(user_id__in=possible_users, vote=GoodVotes.LIKE).values("parent_id")
    goods_ids = [good['parent_id'] for good in likes]
    own_goods_query = Q(id__in=goods_ids, is_deleted=False, status=Good.STATUS_PUBLISHED)
    own_goods_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.good_creator.only('pk').filter(own_goods_query)

def get_timeline_featured_video_likes(user):
    """ лента видеозаписей, которые понравились друзьям пользователя и тем, на кого он подписан """
    possible_users = user.get_friends_and_followings_ids()
    likes = VideoVotes.objects.filter(user_id__in=possible_users, vote=VideoVotes.LIKE).values("parent_id")
    videos_ids = [video['parent_id'] for video in likes]
    own_videos_query = Q(id__in=videos_ids, is_deleted=False, is_public=True)
    own_videos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.video_creator.only('pk').filter(own_videos_query)
