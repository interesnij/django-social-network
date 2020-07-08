from goods.view.community import *
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', CommunityGoods.as_view(), name="community_goods"),
	url(r'^good/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityGood.as_view(), name='community_good'),
	url(r'^add/(?P<pk>\d+)/$', GoodCommunityCreate.as_view()),
	url(r'^add_attach/(?P<pk>\d+)/$', GoodCommunityCreateAttach.as_view())
]
