from django.conf.urls import url
from main.views import MainPageView, ComingView
from main.models import Item


urlpatterns = [
	url(r'^$', ComingView.as_view(), name="coming"),
	url(r'^main/$', MainPageView.as_view(), name="main"),
	url(r'^like/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Item, vote_type=LikeDislike.LIKE)),name='like'),
    url(r'^dislike/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Item, vote_type=LikeDislike.DISLIKE)),name='dislike'),
    url(r'^comment/(?P<pk>\d+)/like/$',login_required(VotesView.as_view(model=Item, vote_type=LikeDislike.LIKE)),name='comment_like'),
    url(r'^comment/(?P<pk>\d+)/dislike/$',login_required(VotesView.as_view(model=Item, vote_type=LikeDislike.DISLIKE)),name='comment_dislike'),
]
