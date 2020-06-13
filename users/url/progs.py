from django.conf.urls import url
from users.views.progs import UserBanCreate, UserUnbanCreate, UserColorChange, UserPostView, PhoneSend, PhoneVerify
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^block/(?P<pk>\d+)/$', login_required(UserBanCreate.as_view())),
    url(r'^unblock/(?P<pk>\d+)/$', login_required(UserUnbanCreate.as_view())),
    url(r'^color/(?P<color>[\w\-]+)/$', login_required(UserColorChange.as_view())),
    url(r'^post_view/(?P<pk>\d+)/$', UserPostView.as_view()),
    url(r'^phone_send/(?P<phone>\d+)/$', login_required(PhoneSend.as_view())),
    url(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', login_required(PhoneVerify.as_view())),
]
