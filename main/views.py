import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from common.template.user import get_detect_main_template
from common.user_progs.timelines_post import get_timeline_posts


class SignupView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			if request.user.is_authenticated:
				self.template_name = "mobile/main/news_list/posts/posts.html"
			else:
				self.template_name = "mobile/main/auth/signup.html"
		else:
			if request.user.is_authenticated:
				self.template_name = "desctop/main/news_list/posts/posts.html"
			else:
				self.template_name = "desctop/main/auth/auth.html"
		return super(SignupView,self).get(request,*args,**kwargs)


class MainPhoneSend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/phone_verification.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainPhoneSend,self).get(request,*args,**kwargs)


class PostsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/posts/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_posts(self.request.user).order_by('-created')
		else:
			items = []
		return items
