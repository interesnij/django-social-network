from django.urls import re_path
from music.view.manage import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    re_path(r'^temp_list/(?P<pk>\d+)/$', login_required(TempListOn.as_view())),
    re_path(r'^temp_genre/(?P<pk>\d+)/$', login_required(TempGenreOn.as_view())),
]
