from django.conf.urls import url
from main.view.comments import *


urlpatterns = [
    url(r'^posts/$', PostCommentsView.as_view(), name="post_comments_list"),
	url(r'^photos/$', PhotoCommentsView.as_view(), name="photo_comments_list"),
	url(r'^goods/$', GoodCommentsView.as_view(), name="good_comments_list"),
	url(r'^video/$', VideoCommentsView.as_view(), name="video_comments_list"),

    url(r'^featured_posts/$', FeaturedPostCommentsView.as_view(), name="featured_post_comments_list"),
	url(r'^featured_photos/$', FeaturedPhotoCommentsView.as_view(), name="featured_photo_comments_list"),
	url(r'^featured_goods/$', FeaturedGoodCommentsView.as_view(), name="featured_good_comments_list"),
	url(r'^featured_video/$', FeaturedVideoCommentsView.as_view(), name="featured_video_comments_list"),
]
