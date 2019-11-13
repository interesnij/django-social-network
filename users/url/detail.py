from django.conf.urls import url
from users.views.detail import AllUsers, ProfileUserView, ItemListView, UserItemView


urlpatterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
    url(r'^item/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserItemView.as_view(), name='user_item'),
    url(r'^list/(?P<pk>\d+)/$', ItemListView.as_view(), name="user_item_list"),

]
