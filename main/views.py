from django.views.generic.base import TemplateView
from main.models import Item
from django.views.generic import ListView



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
	paginate_by=10

	def get(self,request,*args,**kwargs):
		return super(NewsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		self.user=self.request.user
		if self.user.is_authenticated:
			items = self.user.get_timeline_posts().order_by('-created')
		else:
			items=None
		return items

	def get_context_data(self, **kwargs):
		context = super(NewsListView, self).get_context_data(**kwargs)
		return context


class ComingView(TemplateView):
	template_name="main/coming.html"
