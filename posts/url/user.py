from django.conf.urls import url
from posts.view.user import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostUserDetail.as_view(), name="user_item_detail"),
	url(r'^load_post/(?P<uuid>[0-9a-f-]+)/$', PostLoadView.as_view()),
]
