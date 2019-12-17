from django.views.generic.base import TemplateView
from main.models import Item
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


class MainPageView(TemplateView):
	template_name=None
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name="main/mainpage.html"
		else:
			self.template_name="main/auth.html"
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(MainPageView,self).get_context_data(**kwargs)
		return context


class NewsListView(ListView):
	template_name="news_list.html"
	model=Item
	paginate_by=12

	def get_queryset(self):
		self.user=self.request.user
		if self.user.is_authenticated:
			items = self.user.get_timeline_posts().order_by('-created')
		else:
			items=None
		return items


class ComingView(TemplateView):
	template_name="main/coming.html"
