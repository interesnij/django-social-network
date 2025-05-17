from django.urls import re_path
from chat.view.user_progs import *


urlpatterns = [
    re_path(r'^send_page_message/(?P<pk>\d+)/$', UserSendPageMessage.as_view()),
    re_path(r'^send_message/(?P<pk>\d+)/$', UserSendMessage.as_view()),
    re_path(r'^send_voice_message/(?P<pk>\d+)/$', UserSendVoiceMessage.as_view()),
    re_path(r'^save_draft_message/(?P<pk>\d+)/$', UserSaveDraftMessage.as_view()),
    re_path(r'^edit_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageEdit.as_view()),
    re_path(r'^load_chat_message/(?P<uuid>[0-9a-f-]+)/$', LoadUserChatMessage.as_view()),
    re_path(r'^load_message/(?P<uuid>[0-9a-f-]+)/$', LoadUserMessage.as_view()),
    re_path(r'^fixed_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageFixed.as_view()),
    re_path(r'^unfixed_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageUnFixed.as_view()),
    re_path(r'^favorite_messages/$', UserMessagesFavorite.as_view()),
    re_path(r'^unfavorite_messages/$', UserMessagesUnFavorite.as_view()),
    re_path(r'^delete_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageDelete.as_view()),
	re_path(r'^restore_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageRecover.as_view()),

    re_path(r'^create_chat/(?P<pk>\d+)/$', CreateUserChat.as_view()),
    re_path(r'^add_attach_photo/$', PhotoAttachInChatUserCreate.as_view()),
    re_path(r'^(?P<pk>\d+)/add_admin/(?P<user_pk>\d+)/$', UserChatAdminCreate.as_view()),
    re_path(r'^(?P<pk>\d+)/remove_admin/(?P<user_pk>\d+)/$', UserChatAdminDelete.as_view()),
    re_path(r'^(?P<pk>\d+)/remove_member/(?P<user_pk>\d+)/$', UserChatMemberDelete.as_view()),
    re_path(r'^beep_off/(?P<pk>\d+)/$', UserChatBeepOff.as_view()),
    re_path(r'^beep_on/(?P<pk>\d+)/$', UserChatBeepOn.as_view()),
    re_path(r'^exit_user_from_user_chat/(?P<pk>\d+)/$', ExitUserFromUserChat.as_view()),
    re_path(r'^delete_support_chat/(?P<pk>\d+)/$', DeleteSupportChat.as_view()),
    re_path(r'^refresh_support_chat/(?P<pk>\d+)/$', RefreshSupportChat.as_view()),

    re_path(r'^invite_members/$', InviteMembersInUserChat.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/$', UserChatEdit.as_view()),
    re_path(r'^private/(?P<pk>\d+)/$', UserChatPrivate.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', UserChatDelete.as_view()),
	re_path(r'^restore/(?P<pk>\d+)/$', UserChatRecover.as_view()),
    re_path(r'^clean_messages/(?P<pk>\d+)/$', UserChatCleanMessages.as_view()),

    re_path(r'^load_include_users/(?P<pk>\d+)/$', UserChatIncludeUsers.as_view()),
    re_path(r'^load_exclude_users/(?P<pk>\d+)/$', UserChatExcludeUsers.as_view()),

    re_path(r'^like_manager/(?P<pk>\d+)/$', SupportLikeCreate.as_view()),
    re_path(r'^dislike_manager/(?P<pk>\d+)/$', SupportDislikeCreate.as_view()),
]
