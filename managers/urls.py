from django.urls import re_path, include
from managers.views import *


urlpatterns = [
    re_path(r'^$', ManagersView.as_view(), name='managers'),
    re_path(r'^high_officer/$', SuperManagersView.as_view(), name='super_managers'),
    re_path(r'^support/$', SupportChats.as_view()),

    re_path(r'^create_sanction/$', SanctionItemCreate.as_view()),
    re_path(r'^delete_sanction/$', SanctionItemDelete.as_view()),
    re_path(r'^rejected_claims/$', RejectedItemClaims.as_view()),
    re_path(r'^unverify_sanction/$', UnverifyItemCreate.as_view()),
    re_path(r'^send_messages/$', SendManagerMessages.as_view()),

    re_path(r'^moderation_list/', include('managers.url.moderation_list')),
    re_path(r'^penalty_list/', include('managers.url.penalty_list')),
]
