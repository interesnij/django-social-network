import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good, GoodList
from users.models import User
from stst.models import GoodNumbers
from django.http import Http404


class GoodUserDetail(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_item, get_template_anon_user_item

		self.good, self.user = Good.objects.get(pk=self.kwargs["good_pk"]), User.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.post, "goods/u_good/", "detail.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user_item(self.post, "goods/u_good/anon_detail.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodUserDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GoodUserDetail,self).get_context_data(**kwargs)
		context["object"], context["user"] = self.good, self.user
		return context
