from django.conf.urls import url
from posts.view.user import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^detail/(?P<pk>\d+)/$', PostUserDetail.as_view(), name="user_item_detail"),
	url(r'^load_post/(?P<pk>\d+)/$', PostLoadView.as_view()),
]
