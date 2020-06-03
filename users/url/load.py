from django.conf.urls import url
from users.views.load import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^img_load/$', login_required(UserImagesList.as_view())),
    url(r'^video_load/$', login_required(UserVideoList.as_view())),
]
