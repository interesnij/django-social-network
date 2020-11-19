from django.conf.urls import url
from main.view.dislike import *


urlpatterns = [
    url(r'^posts/$', PostDislikesView.as_view(), name="post_dislikes_list"),
	url(r'^photos/$', PhotoDislikesView.as_view(), name="photo_dislikes_list"),
	url(r'^goods/$', GoodDislikesView.as_view(), name="good_dislikes_list"),
	url(r'^video/$', VideoDislikesView.as_view(), name="video_dislikes_list"),

    url(r'^featured_posts/$', FeaturedPostDislikesView.as_view(), name="featured_post_dislikes_list"),
	url(r'^featured_photos/$', FeaturedPhotoDislikesView.as_view(), name="featured_photo_dislikes_list"),
	url(r'^featured_goods/$', FeaturedGoodDislikesView.as_view(), name="featured_good_dislikes_list"),
	url(r'^featured_video/$', FeaturedVideoDislikesView.as_view(), name="featured_video_dislikes_list"),
]
