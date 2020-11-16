from django.conf.urls import url, include
from main.view.featured import *


urlpatterns = [
	url(r'^$', FeaturedPostsView.as_view(), name="featured_posts_list"),
	url(r'^photos/$', FeaturedPhotosView.as_view(), name="featured_photos_list"),
	url(r'^goods/$', FeaturedGoodsView.as_view(), name="featured_goods_list"),
	url(r'^videos/$', FeaturedVideosView.as_view(), name="featured_videos_list"),
	url(r'^audios/$', FeaturedAudiosView.as_view(), name="featured_audios_list"),
]
