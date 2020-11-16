from django.db.models import Q
from posts.models import Post
from gallery.models import Photo
from goods.models import Good
from video.models import Video
from common.model.votes import PostVotes, PhotoVotes, GoodVotes, VideoVotes


def get_timeline_post_likes_for_user(user):
    likes = PostVotes.objects.filter(user_id=user.pk, vote=PostVotes.LIKE).values("parent_id")
    posts_ids = [post['parent_id'] for post in likes]
    own_posts_query = Q(id__in=posts_ids, is_deleted=False, status=Post.STATUS_PUBLISHED)
    own_posts_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.post_creator.only('pk').filter(own_posts_query)

def get_timeline_photo_likes_for_user(user):
    likes = PhotoVotes.objects.filter(user_id=user.pk, vote=PhotoVotes.LIKE).values("parent_id")
    photos_ids = [photo['parent_id'] for photo in likes]
    own_photos_query = Q(id__in=photos_ids, is_deleted=False, is_public=True)
    own_photos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.photo_creator.only('pk').filter(own_photos_query)

def get_timeline_good_likes_for_user(user):
    likes = GoodVotes.objects.filter(user_id=user.pk, vote=GoodVotes.LIKE).values("parent_id")
    goods_ids = [good['parent_id'] for good in likes]
    own_goods_query = Q(id__in=goods_ids, is_deleted=False, status=Good.STATUS_PUBLISHED)
    own_goods_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.good_creator.only('pk').filter(own_goods_query)

def get_timeline_video_likes_for_user(user):
    likes = VideoVotes.objects.filter(user_id=user.pk, vote=VideoVotes.LIKE).values("parent_id")
    videos_ids = [video['parent_id'] for video in likes]
    own_videos_query = Q(id__in=videos_ids, is_deleted=False, is_public=True)
    own_videos_query.add(~Q(Q(creator__blocked_by_users__blocker_id=user.pk) | Q(creator__user_blocks__blocked_user_id=user.pk)), Q.AND)
    return user.video_creator.only('pk').filter(own_videos_query)
