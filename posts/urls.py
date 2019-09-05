from posts.views import PostsView, PostUserCreate
from django.conf.urls import url

urlpatterns = [
    url(r'^posts/$', PostsView.as_view(), name='posts'),
    url(r'^(?P<pk>\d+)/add/$', PostUserCreate.as_view(), name="post_add_user"),
]
