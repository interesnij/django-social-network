import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good, GoodList
from users.models import User
from stst.models import GoodNumbers
from django.http import Http404


class UserGood(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_item, get_template_anon_user_item

		self.good, self.list = Good.objects.get(pk=self.kwargs["pk"]), GoodList.objects.get(uuid=self.kwargs["uuid"])
		self.goods, self.user, user_agent = self.list.get_goods(), self.list.creator, request.META['HTTP_USER_AGENT']
		try:
			GoodNumbers.objects.get(user=request.user.pk, good=self.good.pk)
		except:
			GoodNumbers.objects.create(user=request.user.pk, good=self.good.pk, device=request.user.get_device())
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.post, "goods/u_good/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user_item(self.post, "goods/u_good/anon_good.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserGood,self).get_context_data(**kwargs)
		context["object"] = self.good
		context["list"] = self.list
		context["user"] = self.user
		context["next"] = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
		context["prev"] = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
		return context


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
