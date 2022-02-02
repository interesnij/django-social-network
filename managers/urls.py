from django.conf.urls import url, include
from managers.views import *


urlpatterns = [
    url(r'^$', ManagersView.as_view(), name='managers'),
    url(r'^high_officer/$', SuperManagersView.as_view(), name='super_managers'),

    url(r'^add_admin/(?P<pk>\d+)/$', UserAdministratorCreate.as_view()),
    url(r'^delete_admin/(?P<pk>\d+)/$', UserAdministratorDelete.as_view()),
    url(r'^add_advertiser/(?P<pk>\d+)/$', UserAdvertiserCreate.as_view()),
    url(r'^delete_advertiser/(?P<pk>\d+)/$', UserAdvertiserDelete.as_view()),

    url(r'^add_high_manager/(?P<pk>\d+)/$', UserHighManagerCreate.as_view()),
    url(r'^delete_high_manager/(?P<pk>\d+)/$', UserHighManagerDelete.as_view()),
    url(r'^add_manager/(?P<pk>\d+)/$', UserManagerCreate.as_view()),
    url(r'^delete_manager/(?P<pk>\d+)/$', UserManagerDelete.as_view()),
    url(r'^add_trainee_manager/(?P<pk>\d+)/$', UserTraineeManagerCreate.as_view()),
    url(r'^delete_trainee_manager/(?P<pk>\d+)/$', UserTraineeManagerDelete.as_view()),

    url(r'^add_support/(?P<pk>\d+)/$', UserSupportCreate.as_view()),
    url(r'^delete_support/(?P<pk>\d+)/$', UserSupportDelete.as_view()),
    url(r'^add_trainee_support/(?P<pk>\d+)/$', UserTraineeSupportCreate.as_view()),
    url(r'^delete_trainee_support/(?P<pk>\d+)/$', UserTraineeSupportDelete.as_view()),

    url(r'^add_moderator/(?P<pk>\d+)/$', UserModeratorCreate.as_view()),
    url(r'^delete_moderator/(?P<pk>\d+)/$', UserModeratorDelete.as_view()),
    url(r'^add_trainee_moderator/(?P<pk>\d+)/$', UserTraineeModeratorCreate.as_view()),
    url(r'^delete_trainee_moderator/(?P<pk>\d+)/$', UserTraineeModeratorDelete.as_view()),

    url(r'^moderation_list/', include('managers.url.moderation_list')),
    url(r'^penalty_list/', include('managers.url.penalty_list')),

    url(r'^send_messages/$', SendManagerMessages.as_view()),
]
