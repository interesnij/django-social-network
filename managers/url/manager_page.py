from django.conf.urls import url
from managers.view.managers import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user_admin/(?P<pk>\d+)/$', login_required(UserAdminList.as_view())),
    url(r'^community_admin/(?P<pk>\d+)/$', login_required(CommunityAdminList.as_view())),
    url(r'^post_admin/(?P<pk>\d+)/$', login_required(PostAdminList.as_view())),
    url(r'^photo_admin/(?P<pk>\d+)/$', login_required(PhotoAdminList.as_view())),
    url(r'^good_admin/(?P<pk>\d+)/$', login_required(GoodAdminList.as_view())),
    url(r'^audio_admin/(?P<pk>\d+)/$', login_required(AudioAdminList.as_view())),
    url(r'^video_admin/(?P<pk>\d+)/$', login_required(VideoAdminList.as_view())),

    url(r'^user_editor/(?P<pk>\d+)/$', login_required(UserEditorList.as_view())),
    url(r'^community_editor/(?P<pk>\d+)/$', login_required(CommunityEditorList.as_view())),
    url(r'^post_editor/(?P<pk>\d+)/$', login_required(PostEditorList.as_view())),
    url(r'^photo_editor/(?P<pk>\d+)/$', login_required(PhotoEditorList.as_view())),
    url(r'^good_editor/(?P<pk>\d+)/$', login_required(GoodEditorList.as_view())),
    url(r'^audio_editor/(?P<pk>\d+)/$', login_required(AudioEditorList.as_view())),
    url(r'^video_editor/(?P<pk>\d+)/$', login_required(VideoEditorList.as_view())),
]
