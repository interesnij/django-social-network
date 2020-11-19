from django.db.models import Q
from posts.models import Post
from gallery.models import Photo
from goods.models import Good
from video.models import Video
from common.model.votes import PostVotes, PhotoVotes, GoodVotes, VideoVotes


def get_timeline_post_dislikes(user):
    """ лента записей, которые не понравились пользователю """
    dislikes = PostVotes.objects.filter(user_id=user.pk, vote=PostVotes.DISLIKE).values("parent_id")
    posts_ids = [post['parent_id'] for post in dislikes]
    own_posts_query = Q(id__in=posts_ids, is_deleted=False, status=Post.STATUS_PUBLISHED)
    own_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.post_creator.only('pk').filter(own_posts_query)

def get_timeline_photo_dislikes(user):
    """ лента фотографий, которые не понравились пользователю """
    dislikes = PhotoVotes.objects.filter(user_id=user.pk, vote=PhotoVotes.DISLIKE).values("parent_id")
    photos_ids = [photo['parent_id'] for photo in dislikes]
    own_photos_query = Q(id__in=photos_ids, is_deleted=False, is_public=True)
    own_photos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.photo_creator.only('pk').filter(own_photos_query)

def get_timeline_good_dislikes(user):
    """ лента товаров, которые не понравились пользователю """
    dislikes = GoodVotes.objects.filter(user_id=user.pk, vote=GoodVotes.DISLIKE).values("parent_id")
    goods_ids = [good['parent_id'] for good in dislikes]
    own_goods_query = Q(id__in=goods_ids, is_deleted=False, status=Good.STATUS_PUBLISHED)
    own_goods_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.good_creator.only('pk').filter(own_goods_query)

def get_timeline_video_dislikes(user):
    """ лента видеозаписей, которые не понравились пользователю """
    dislikes = VideoVotes.objects.filter(user_id=user.pk, vote=VideoVotes.DISLIKE).values("parent_id")
    videos_ids = [video['parent_id'] for video in dislikes]
    own_videos_query = Q(id__in=videos_ids, is_deleted=False, is_public=True)
    own_videos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.video_creator.only('pk').filter(own_videos_query)


def get_timeline_featured_post_dislikes(user):
    """ лента записей, которые понравились друзьям пользователя и тем, на кого он подписан """
    possible_users = user.get_friends_and_followings_ids()
    dislikes = PostVotes.objects.filter(user_id__in=possible_users, vote=PostVotes.DISLIKE).values("parent_id")
    posts_ids = [post['parent_id'] for post in dislikes]
    own_posts_query = Q(id__in=posts_ids, is_deleted=False, status=Post.STATUS_PUBLISHED)
    own_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.post_creator.only('pk').filter(own_posts_query)

def get_timeline_featured_photo_dislikes(user):
    """ лента фотографий, которые понравились друзьям пользователя и тем, на кого он подписан """
    possible_users = user.get_friends_and_followings_ids()
    dislikes = PhotoVotes.objects.filter(user_id__in=possible_users, vote=PhotoVotes.DISLIKE).values("parent_id")
    photos_ids = [photo['parent_id'] for photo in dislikes]
    own_photos_query = Q(id__in=photos_ids, is_deleted=False, is_public=True)
    own_photos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.photo_creator.only('pk').filter(own_photos_query)

def get_timeline_featured_good_dislikes(user):
    """ лента товаров, которые понравились друзьям пользователя и тем, на кого он подписан """
    possible_users = user.get_friends_and_followings_ids()
    dislikes = GoodVotes.objects.filter(user_id__in=possible_users, vote=GoodVotes.DISLIKE).values("parent_id")
    goods_ids = [good['parent_id'] for good in dislikes]
    own_goods_query = Q(id__in=goods_ids, is_deleted=False, status=Good.STATUS_PUBLISHED)
    own_goods_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.good_creator.only('pk').filter(own_goods_query)

def get_timeline_featured_video_dislikes(user):
    """ лента видеозаписей, которые понравились друзьям пользователя и тем, на кого он подписан """
    possible_users = user.get_friends_and_followings_ids()
    dislikes = VideoVotes.objects.filter(user_id__in=possible_users, vote=VideoVotes.DISLIKE).values("parent_id")
    videos_ids = [video['parent_id'] for video in dislikes]
    own_videos_query = Q(id__in=videos_ids, is_deleted=False, is_public=True)
    own_videos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.video_creator.only('pk').filter(own_videos_query)
