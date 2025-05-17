from django.urls import re_path
from users.views.settings import *


urlpatterns = [
    re_path(r'^$', UserGeneralChange.as_view(), name='user_general_form'),
    re_path(r'^info/$', UserInfoChange.as_view(), name='user_info_form'),
    re_path(r'^design/$', UserDesign.as_view(), name='user_design_form'),

    re_path(r'^notify/$', UserNotifyView.as_view(), name='user_profile_notify'),
    re_path(r'^notify_post/$', UserNotifyPostView.as_view(), name='user_post_notify'),
    re_path(r'^notify_photo/$', UserNotifyPhotoView.as_view(), name='user_photo_notify'),
    re_path(r'^notify_good/$', UserNotifyGoodView.as_view(), name='user_good_notify'),
    re_path(r'^notify_video/$', UserNotifyVideoView.as_view(), name='user_video_notify'),
    re_path(r'^notify_music/$', UserNotifyMusicView.as_view(), name='user_music_notify'),

    re_path(r'^private/$', UserPrivateView.as_view(), name='user_profile_private'),
    re_path(r'^load_include_users/$', UserPrivateIncludeUsers.as_view()),
    re_path(r'^load_exclude_users/$', UserPrivateExcludeUsers.as_view()),

    re_path(r'^edit_name/$', UserEditName.as_view()),
    re_path(r'^edit_password/$', UserEditPassword.as_view()),
    re_path(r'^edit_email/$', UserEditEmail.as_view()),
    re_path(r'^edit_phone/$', UserEditPhone.as_view()),
    re_path(r'^edit_link/$', UserEditLink.as_view()),
    re_path(r'^verify_send/$', UserVerifySend.as_view()),
    re_path(r'^identify_send/$', UserIdentifySend.as_view()),
    re_path(r'^remove_profile/$', UserRemoveProfile.as_view()),
]
