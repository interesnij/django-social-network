from django.conf.urls import url
from users.views.load import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^u_img_load/$', login_required(UserLoadPhoto.as_view()), name="u_photo_load"),
    url(r'^u_album_img_load/(?P<uuid>[0-9a-f-]+)/$', login_required(UserLoadPhotoAlbum.as_view()), name="u_photo_list_load"),

    url(r'^u_img_comment_load/$', login_required(UserLoadPhotoComment.as_view())),
    url(r'^u_video_load/$', login_required(UserLoadVideo.as_view())),

    url(r'^u_music_load/$', login_required(UserLoadMusic.as_view()), name="u_music_load"),
    url(r'^u_music_list_load/(?P<uuid>[0-9a-f-]+)/$', login_required(UserLoadMusicList.as_view()), name="u_music_list_load"),

    url(r'^u_article_load/$', login_required(UserLoadArticle.as_view())),
    url(r'^u_good_load/$', login_required(UserLoadGood.as_view())),

    url(r'^c_img_load/$', login_required(CommunityLoadPhoto.as_view())),
    url(r'^c_img_comment_load/$', login_required(CommunityLoadPhotoComment.as_view())),
    url(r'^c_video_load/$', login_required(CommunityLoadVideo.as_view())),
    url(r'^c_music_load/$', login_required(CommunityLoadMusic.as_view())),
    url(r'^c_article_load/$', login_required(CommunityLoadArticle.as_view())),
    url(r'^c_good_load/$', login_required(CommunityLoadGood.as_view())),
]
