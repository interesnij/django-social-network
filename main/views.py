from django.views.generic.base import TemplateView
from django.views.generic import ListView


class MainPageView(TemplateView):
	template_name=None
	def get(self,request,*args,**kwargs):
		from common.utils import is_mobile

		if request.user.is_authenticated:
			if is_mobile(request):
				self.template_name="main/mob_news.html"
			else:
				self.template_name="main/news.html"
		else:
			if is_mobile(request):
				self.template_name="main/mob_auth.html"
			else:
				self.template_name="main/auth.html"
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
