from django.urls import re_path, include
from main.views import *


urlpatterns = [
	re_path(r'^phone_verify/$', MainPhoneSend.as_view(), name="phone_send"),
	re_path(r'^services/$', MainServicesView.as_view(), name="main_services"),

	re_path(r'^$', NewsListView.as_view(), name="news_list"),
	re_path(r'^featured/$', FeaturedListView.as_view(), name="featured_list"),
	re_path(r'^load_custom_link/$', LoadCustomLink.as_view()),
	re_path(r'^comments/', include('main.url.comments')),
	re_path(r'^items/', include('main.url.items')),
]
