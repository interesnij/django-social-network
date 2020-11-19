from django.conf.urls import url, include
from main.view.posts import *


urlpatterns = [
	url(r'^photos/$', PhotosView.as_view(), name="photos_list"),
	url(r'^goods/$', GoodsView.as_view(), name="goods_list"),
	url(r'^videos/$', VideosView.as_view(), name="videos_list"),
	url(r'^music/$', AudiosView.as_view(), name="music_list"),

	url(r'^featured_posts/$', FeaturedPostsView.as_view(), name="featured_posts_list"),
	url(r'^featured_photos/$', FeaturedPhotosView.as_view(), name="featured_photos_list"),
	url(r'^featured_goods/$', FeaturedGoodsView.as_view(), name="featured_goods_list"),
	url(r'^featured_videos/$', FeaturedVideosView.as_view(), name="featured_videos_list"),
	url(r'^featured_music/$', FeaturedAudiosView.as_view(), name="featured_music_list"),
]
