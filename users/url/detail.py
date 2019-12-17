from django.conf.urls import url
from users.views.detail import AllUsers, ItemListView, UserItemView, AllCommonUsers, AllUsersLists, AllUsers


urlpatterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^all_users_list/$', AllUsersList.as_view(), name='all_users_list'),
    url(r'^common-users/(?P<pk>\d+)/$', AllCommonUsers.as_view(), name='all_common_users'),
    url(r'^item/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserItemView.as_view(), name='user_item'),
    url(r'^list/(?P<pk>\d+)/$', ItemListView.as_view(), name="user_item_list"),

]
