from django.conf.urls import url
from users.views.load import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^img_load/$', login_required(UserPhotosList.as_view())),
    url(r'^img_comment_load/$', login_required(UserPhotosCommentList.as_view())),
    url(r'^video_load/$', login_required(UserVideosList.as_view())),
    url(r'^music_load/$', login_required(UserMusicsList.as_view())),
    url(r'^article_load/$', login_required(UserArticlesList.as_view())),
    url(r'^good_load/$', login_required(UserGoodsList.as_view())),
]
