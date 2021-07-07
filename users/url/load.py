from django.conf.urls import url
from users.views.load import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^u_img_load/$', login_required(UserLoadPhoto.as_view()), name="u_photo_load"),
    url(r'^u_photo_list_load/(?P<uuid>[0-9a-f-]+)/$', login_required(UserLoadPhotoList.as_view()), name="u_photo_list_load"),

    url(r'^u_img_comment_load/$', login_required(UserLoadPhotoComment.as_view()), name="u_photo_comment_load"),

    url(r'^u_video_load/$', login_required(UserLoadVideo.as_view()), name="u_video_load"),
    url(r'^u_video_list_load/(?P<uuid>[0-9a-f-]+)/$', login_required(UserLoadVideoList.as_view()), name="u_video_list_load"),

    url(r'^u_doc_load/$', login_required(UserLoadDoc.as_view()), name="u_doc_load"),
    url(r'^u_doc_list_load/(?P<uuid>[0-9a-f-]+)/$', login_required(UserLoadDocList.as_view()), name="u_doc_list_load"),

    url(r'^u_music_load/$', login_required(UserLoadMusic.as_view()), name="u_music_load"),
    url(r'^u_music_list_load/(?P<uuid>[0-9a-f-]+)/$', login_required(UserLoadMusicList.as_view()), name="u_music_list_load"),

    url(r'^u_article_load/$', login_required(UserLoadArticle.as_view())),
    url(r'^u_survey_load/$', login_required(UserLoadSurvey.as_view()), name="u_survey_load"),
    url(r'^u_survey_list_load/(?P<uuid>[0-9a-f-]+)/$', login_required(UserLoadSurveyList.as_view()), name="u_survey_list_load"),

    url(r'^u_good_load/$', login_required(UserLoadGood.as_view()), name="u_good_load"),
    url(r'^u_good_list_load/(?P<uuid>[0-9a-f-]+)/$', login_required(UserLoadGoodList.as_view()), name="u_good_list_load"),

    url(r'^chat_items/$', login_required(ChatItemsLoad.as_view())),
    url(r'^communities/$', login_required(CommunitiesLoad.as_view())),
    url(r'^friends/$', login_required(FriendsLoad.as_view())),
    url(r'^smiles/$', SmilesLoad.as_view()),
    url(r'^smiles_stickers/$', SmilesStickersLoad.as_view()),
]
