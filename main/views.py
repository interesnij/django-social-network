from django.views.generic.base import TemplateView
from django.views.generic import ListView
from main.models import Item


class MainPageView(TemplateView):
	template_name=None

	def get(self,request,*args,**kwargs):

		if request.user.is_authenticated and not request.user.is_phone_verified:
			self.template_name="main/phone_verification.html"
		elif request.user.is_authenticated and request.user.is_phone_verified:
			self.template_name="main/news.html"
		else:
			self.template_name="main/auth.html"
		MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			"mob_" + self.template_name
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(MainPageView,self).get_context_data(**kwargs)
		return context


class NewsListView(ListView):
	from main.models import Item

	template_name="news_list.html"
	model=Item
	paginate_by=30

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = self.request.user.get_timeline_posts().order_by('-created')
		else:
			items=None
		return items


class ComingView(TemplateView):
	template_name="base_coming.html"


class MainPhoneSend(TemplateView):
	template_name="phone_verification.html"
