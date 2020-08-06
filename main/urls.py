from django.conf.urls import url
from main.views import *


urlpatterns = [
	url(r'^$', ComingView.as_view(), name="coming"),
	url(r'^phone_send/$', MainPhoneSend.as_view(), name="phone_send"),

	url(r'^posts/$', PostsListView.as_view(), name="post_list"),
	url(r'^featured_posts/$', FeaturedPostsView.as_view(), name="featured_posts_list"),
	url(r'^photos/$', PhotosListView.as_view(), name="photos_list"),
	url(r'^featured_photos/$', FeaturedPhotosView.as_view(), name="featured_photos_list"),
	url(r'^goods/$', GoodsListView.as_view(), name="goods_list"),
	url(r'^featured_goods/$', FeaturedGoodsView.as_view(), name="featured_goods_list"),
	url(r'^videos/$', VideosListView.as_view(), name="videos_list"),
	url(r'^featured_videos/$', FeaturedVideosView.as_view(), name="featured_videos_list"),
	url(r'^audios/$', AudiosListView.as_view(), name="audios_list"),
	url(r'^featured_audios/$', FeaturedAudiosView.as_view(), name="featured_audios_list"),
]
