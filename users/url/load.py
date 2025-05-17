from django.urls import re_path
from users.views.load import *


urlpatterns = [
    re_path(r'^u_img_load/$', UserLoadPhoto.as_view(), name="u_photo_load"),
    re_path(r'^u_photo_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadPhotoList.as_view(), name="u_photo_list_load"),
    re_path(r'^u_img_comment_load/$', UserLoadPhotoComment.as_view(), name="u_photo_comment_load"),
    re_path(r'^u_img_message_load/$', UserLoadPhotoMessage.as_view(), name="u_photo_comment_load"),

    re_path(r'^u_video_load/$', UserLoadVideo.as_view(), name="u_video_load"),
    re_path(r'^u_video_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadVideoList.as_view(), name="u_video_list_load"),

    re_path(r'^u_doc_load/$', UserLoadDoc.as_view(), name="u_doc_load"),
    re_path(r'^u_doc_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadDocList.as_view(), name="u_doc_list_load"),

    re_path(r'^u_music_load/$', UserLoadMusic.as_view(), name="u_music_load"),
    re_path(r'^u_music_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadMusicList.as_view(), name="u_music_list_load"),

    re_path(r'^u_article_load/$', UserLoadArticle.as_view()),

    re_path(r'^u_survey_load/$', UserLoadSurvey.as_view(), name="u_survey_load"),
    re_path(r'^u_survey_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadSurveyList.as_view(), name="u_survey_list_load"),

    re_path(r'^u_good_load/$', UserLoadGood.as_view(), name="u_good_load"),
    re_path(r'^u_good_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadGoodList.as_view(), name="u_good_list_load"),

    re_path(r'^post_lists/$', PostListsLoad.as_view()),
    re_path(r'^communities_post_lists/$', CommunitiesPostListsLoad.as_view()),
    re_path(r'^chat_items/$', ChatItemsLoad.as_view()),

    re_path(r'^friends/$', FriendsLoad.as_view()),
    re_path(r'^smiles/$', SmilesLoad.as_view()),
    re_path(r'^smiles_stickers/$', SmilesStickersLoad.as_view()),
    re_path(r'^chats/$', ChatsLoad.as_view()),
    re_path(r'^communities/$', CommunitiesLoad.as_view()),

    re_path(r'^list_include_users/$', LoadListIncludeUsers.as_view()),
    re_path(r'^list_exclude_users/$', LoadListExcludeUsers.as_view()),
]
