from django.conf.urls import url
from main.view.dislike import *


urlpatterns = [
    url(r'^posts/$', PostDislikesListView.as_view(), name="post_dislikes_list"),
	url(r'^photos/$', PhotoDislikesListView.as_view(), name="photo_dislikes_list"),
	url(r'^goods/$', GoodDislikesListView.as_view(), name="good_dislikes_list"),
	url(r'^video/$', VideoDislikesListView.as_view(), name="video_dislikes_list"),
]
