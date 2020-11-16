import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from common.template.user import get_detect_main_template


class SignupView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			if request.user.is_authenticated:
				self.template_name = "mobile/main/news_list/news/posts.html"
			else:
				self.template_name = "mobile/main/auth/signup.html"
		else:
			if request.user.is_authenticated:
				self.template_name = "desctop/main/news_list/news/posts.html"
			else:
				self.template_name = "desctop/main/auth/auth.html"
		return super(SignupView,self).get(request,*args,**kwargs)


class MainPhoneSend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/phone_verification.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainPhoneSend,self).get(request,*args,**kwargs)
