from django.conf.urls import url, include
from managers.views import *


urlpatterns = [
    url(r'^$', ManagersView.as_view(), name='managers'),
    url(r'^high_officer/$', SuperManagersView.as_view(), name='super_managers'),

    url(r'^moderation_list/', include('managers.url.moderation_list')),
    url(r'^penalty_list/', include('managers.url.penalty_list')),

    url(r'^create_sanction/$', SanctionItemCreate.as_view()),
    url(r'^delete_sanction/$', SanctionItemDelete.as_view()),
    url(r'^rejected_claims/$', RejectedItemClaims.as_view()),
    url(r'^unverify_sanction/$', UnverifyItemCreate.as_view()),

    url(r'^send_messages/$', SendManagerMessages.as_view()),
]
