from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from onesignal import OneSignal, SegmentNotification


class MainPageView(TemplateView,CategoryListMixin):
	template_name="main/mainpage.html"
	client = OneSignal("608dcb86-a851-4acf-bca5-a292361bc538", "ZjEwZWU1NDQtZmYyMy00ZTEyLTliYWUtYmVhMTE4Y2U5MWU2")
	notification_to_all_users = SegmentNotification(
    contents={"en": "Hello from OneSignal-Notifications"},
    included_segments=SegmentNotification.ALL
	)
	client.send(notification_to_all_users)

	def get_context_data(self,**kwargs):
		context=super(MainPageView,self).get_context_data(**kwargs)

		return context
