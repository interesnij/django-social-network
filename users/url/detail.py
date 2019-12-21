from django.conf.urls import url
from users.views.detail import *
from users.views.lists import AllUsersList, ItemListView, UserCommunitiesList

urlpatterns = [
    url(r'^all_users_list/$', AllUsersList.as_view(), name='all_users_list'),
    url(r'^item/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserItemView.as_view(), name='user_item'),
    url(r'^communities/(?P<uuid>[0-9a-f-]+)/$', UserCommunitiesList.as_view()),
    url(r'^list/(?P<pk>\d+)/$', ItemListView.as_view(), name="user_item_list"),

]
