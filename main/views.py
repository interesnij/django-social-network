from django.views.generic.base import TemplateView
from django.views.generic import ListView
from main.models import Item


class MainPageView(ListView):
	template_name=None

	def get(self,request,*args,**kwargs):
		from common.utils import is_mobile

		model=Item
		paginate_by=30

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
		return super(ListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(ListView,self).get_context_data(**kwargs)
		return context

	def get_queryset(self):
		news_list = self.request.user.get_timeline_posts().order_by("created")
		return news_list


class ComingView(TemplateView):
	template_name="base_coming.html"
