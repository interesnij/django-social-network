from posts.views import PostsView
from django.conf.urls import url

urlpatterns = [
    url(r'^posts/$', PostsView.as_view(), name='posts')
]
