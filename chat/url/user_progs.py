from django.conf.urls import url, include
from chat.view.user_progs import *


urlpatterns = [
    url(r'^send_page_message/(?P<pk>\d+)/$', UserSendPageMessage.as_view()),
    url(r'^send_message/(?P<pk>\d+)/$', UserSendMessage.as_view()),
    url(r'^save_draft_message/(?P<pk>\d+)/$', UserSaveDraftMessage.as_view()),
    url(r'^edit_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageEdit.as_view()),
    url(r'^load_chat_message/(?P<uuid>[0-9a-f-]+)/$', LoadUserChatMessage.as_view()),
    url(r'^load_message/(?P<uuid>[0-9a-f-]+)/$', LoadUserMessage.as_view()),
    url(r'^fixed_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageFixed.as_view()),
    url(r'^unfixed_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageUnFixed.as_view()),
    url(r'^favorite_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageFavorite.as_view()),
    url(r'^unfavorite_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageUnFavorite.as_view()),
    url(r'^delete_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageDelete.as_view()),
	url(r'^restore_message/(?P<uuid>[0-9a-f-]+)/$', UserMessageRecover.as_view()),

    url(r'^create_chat/(?P<pk>\d+)/$', CreateUserChat.as_view()),
    url(r'^add_attach_photo/$', PhotoAttachInChatUserCreate.as_view()),
    url(r'^(?P<pk>\d+)/add_admin/(?P<user_pk>\d+)/$', UserChatAdminCreate.as_view()),
    url(r'^(?P<pk>\d+)/remove_admin/(?P<user_pk>\d+)/$', UserChatAdminDelete.as_view()),
    url(r'^(?P<pk>\d+)/remove_member/(?P<user_pk>\d+)/$', UserChatMemberDelete.as_view()),
    url(r'^beep_off/(?P<pk>\d+)/$', UserChatBeepOff.as_view()),
    url(r'^beep_on/(?P<pk>\d+)/$', UserChatBeepOn.as_view()),
    url(r'^(?P<pk>\d+)/append_in_chat/(?P<user_pk>\d+)/$', AppendUserInUserChat.as_view()),
    url(r'^(?P<pk>\d+)/exit_user_from_user_chat/(?P<user_pk>\d+)/$', ExitUserFromUserChat.as_view()),

    url(r'^invite_members/(?P<pk>\d+)/$', InviteMembersInUserChat.as_view()),
]
