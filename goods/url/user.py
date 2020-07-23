from goods.view.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', UserGoods.as_view(), name="user_goods"),
	url(r'^good/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserGood.as_view(), name='user_good'),
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', GoodUserCommentList.as_view()),
]
