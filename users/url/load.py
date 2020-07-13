from django.conf.urls import url
from users.views.load import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^u_img_load/$', login_required(UserPhotosList.as_view())),
    url(r'^u_img_comment_load/$', login_required(UserPhotosCommentList.as_view())),
    url(r'^u_video_load/$', login_required(UserVideosList.as_view())),
    url(r'^u_music_load/$', login_required(UserMusicsList.as_view())),
    url(r'^u_article_load/$', login_required(UserArticlesList.as_view())),
    url(r'^u_good_load/$', login_required(UserGoodsList.as_view())),

    url(r'^c_img_load/$', login_required(CommunityPhotosList.as_view())),
    url(r'^c_img_comment_load/$', login_required(CommunityPhotosCommentList.as_view())),
    url(r'^c_video_load/$', login_required(CommunityVideosList.as_view())),
    url(r'^c_music_load/$', login_required(CommunityMusicsList.as_view())),
    url(r'^c_article_load/$', login_required(CommunityArticlesList.as_view())),
    url(r'^c_good_load/$', login_required(CommunityGoodsList.as_view())),
]
