from django.conf.urls import url
from music.views import AllMusicView, AllMusicListView, AllSearchMusicView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', AllMusicView.as_view(), name='all_music'),
    url(r'^all_music_list/$', AllMusicListView.as_view(), name='all_music_list'),
    url(r'^search_music/$', AllSearchMusicView.as_view(), name='search_all_music'),
]
