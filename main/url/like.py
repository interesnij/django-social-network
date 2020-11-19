from django.conf.urls import url
from main.view.like import *


urlpatterns = [
    url(r'^posts/$', PostLikesView.as_view(), name="post_likes_list"),
	url(r'^photos/$', PhotoLikesView.as_view(), name="photo_likes_list"),
	url(r'^goods/$', GoodLikesView.as_view(), name="good_likes_list"),
	url(r'^video/$', VideoLikesView.as_view(), name="video_likes_list"),

    url(r'^featured_posts/$', FeaturedPostLikesView.as_view(), name="featured_post_likes_list"),
	url(r'^featured_photos/$', FeaturedPhotoLikesView.as_view(), name="featured_photo_likes_list"),
	url(r'^featured_goods/$', FeaturedGoodLikesView.as_view(), name="featured_good_likes_list"),
	url(r'^featured_video/$', FeaturedVideoLikesView.as_view(), name="featured_video_likes_list"),
]
