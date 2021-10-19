from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good, GoodList
from communities.models import Community
from common.check.community import check_can_get_lists
from stst.models import GoodNumbers
from django.http import Http404


class CommunityGood(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_community_item, get_template_anon_community_item

		self.list, self.good = GoodList.objects.get(uuid=self.kwargs["uuid"]), Good.objects.get(pk=self.kwargs["pk"])
		self.goods = self.list.get_goods()
		check_can_get_lists(self.request.user, self.list.community)

		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.post, "goods/c_good/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.post, "goods/c_good/anon_good.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityGood,self).get_context_data(**kwargs)
		context["object"] = self.good
		context["list"] = self.list
		context["community"] = self.list.community
		context["next"] = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
		context["prev"] = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
		return context


class GoodCommunityDetail(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_community_item, get_template_anon_community_item

		self.good, self.c = Good.objects.get(pk=self.kwargs["good_pk"]), Community.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.post, "goods/c_good/", "detail.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.post, "goods/c_good/anon_detail.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodCommunityDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GoodCommunityDetail,self).get_context_data(**kwargs)
		context["object"], context["community"] = self.good, self.c
		return context
