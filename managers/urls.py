from django.conf.urls import url, include
from managers.views import *


urlpatterns = [
    url(r'^$', ManagersView.as_view(), name='managers'),
    url(r'^high_officer/$', SuperManagersView.as_view(), name='super_managers'),

    url(r'^moderation_list/', include('managers.url.moderation_list')),
    url(r'^penalty_list/', include('managers.url.penalty_list')),
    url(r'^progs/', include('managers.url.progs')),

    url(r'^send_messages/$', SendManagerMessages.as_view()),
]
