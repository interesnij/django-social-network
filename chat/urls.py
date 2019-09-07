from chat.views import ChatView
from django.conf.urls import url

urlpatterns=[
	url(r'^$', ChatView.as_view(), name="chat"),
]
