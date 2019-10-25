from posts.views import (
                            PostsView,
                            PostDetailView,
                            PostUserCreate,
                            RepostUser,
                        )
from django.conf.urls import url



urlpatterns = [
    url(r'^$', PostsView.as_view(), name='posts'),
    url(r'^add_post/$', PostUserCreate.as_view(), name="post_add_user"),
    url(r'^repost/(?P<uuid>[0-9a-f-]+)/$', RepostUser.as_view(), name="repost_user"),
    url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostDetailView.as_view(), name='post_detail'),
]
