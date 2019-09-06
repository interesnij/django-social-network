from posts.views import PostsView, PostUserHardCreate, PostUserMediumCreate, PostUserLiteCreate
from django.conf.urls import url

urlpatterns = [
    url(r'^posts/$', PostsView.as_view(), name='posts'),
    url(r'^add_hard/$', PostUserHardCreate.as_view(), name="post_add_hard_user"),
    url(r'^add_medium/$', PostUserMediumCreate.as_view(), name="post_add_medium_user"),
    url(r'^add_lite/$', PostUserLiteCreate.as_view(), name="post_add_lite_user"),
]
