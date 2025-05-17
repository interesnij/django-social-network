from django.urls import re_path
from posts.view.user import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	re_path(r'^detail/(?P<pk>\d+)/$', PostUserDetail.as_view(), name="user_item_detail"),
	re_path(r'^load_post/(?P<pk>\d+)/$', PostLoadView.as_view()),
]
