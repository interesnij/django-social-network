from django.conf.urls import url, include
from main.view.news import *


urlpatterns = [
	url(r'^$', PostsListView.as_view(), name="post_list"),
	url(r'^photos/$', PhotosListView.as_view(), name="photos_list"),
	url(r'^goods/$', GoodsListView.as_view(), name="goods_list"),
	url(r'^videos/$', VideosListView.as_view(), name="videos_list"),
	url(r'^audios/$', AudiosListView.as_view(), name="audios_list"),
]
