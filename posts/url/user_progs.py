from django.conf.urls import url
from posts.view.user_progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^add_post/(?P<pk>\d+)/$', login_required(PostUserCreate.as_view())),
]
