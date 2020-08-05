from django.views.generic.base import TemplateView
from django.views.generic import ListView


class MainPageView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="main/", template="news.html", request=request)
		else:
			self.template_name = 'main/auth.html'
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MainPageView,self).get_context_data(**kwargs)
		return context


class NewsListView(ListView):
	template_name = "news_list.html"
	paginate_by = 15

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = self.request.user.get_timeline_posts_for_user().order_by('-created')
		else:
			items = None
		return items

class FeaturedPostsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="main/", template="featured_news.html", request=request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedPostsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = self.request.user.get_timeline_posts_for_possible_users()
		else:
			items = None
		return items


class ComingView(TemplateView):
	template_name = "base_coming.html"


class MainPhoneSend(TemplateView):
	template_name = "phone_verification.html"
