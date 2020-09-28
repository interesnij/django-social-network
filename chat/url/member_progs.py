from django.conf.urls import url, include
from chat.view.member_progs import *


urlpatterns = [
    url(r'^(?P<pk>\d+)/get_members/$', ChatMembers.as_view()),
    url(r'^(?P<pk>\d+)/add_admin/(?P<user_pk>\d+)/$', ChatAdminCreate.as_view()),
    url(r'^(?P<pk>\d+)/remove_admin/(?P<user_pk>\d+)/$', ChatAdminDelete.as_view()),
    url(r'^(?P<pk>\d+)/add_member/(?P<user_pk>\d+)/$', ChatMemberCreate.as_view()),
    url(r'^(?P<pk>\d+)/remove_member/(?P<user_pk>\d+)/$', ChatMemberDelete.as_view()),
]
