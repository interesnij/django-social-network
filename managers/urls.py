from django.conf.urls import url, include
from managers.views import MainManagersView, ManagersView, SuperManagersView


urlpatterns = [
    url(r'^$', MainManagersView.as_view(), name='main_manager'),
    url(r'^(?P<pk>\d+)/$', ManagersView.as_view(), name='managers'),
    url(r'^high_officer/(?P<pk>\d+)/$', SuperManagersView.as_view(), name='super_managers'),

    url(r'^progs_user/', include('managers.url.progs_user')),
    url(r'^progs_community/', include('managers.url.progs_community')),
    url(r'^progs_post/', include('managers.url.progs_post')),
    url(r'^progs_good/', include('managers.url.progs_good')),
    url(r'^progs_photo/', include('managers.url.progs_photo')),
    url(r'^progs_video/', include('managers.url.progs_video')),
    url(r'^progs_audio/', include('managers.url.progs_audio')),

    url(r'^moderation_list/', include('managers.url.moderated_list')),
    url(r'^penalty_list/', include('managers.url.penalty_list')),
]
