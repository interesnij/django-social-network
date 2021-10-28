from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good, GoodList
from communities.models import Community
from common.check.community import check_can_get_lists
from stst.models import GoodNumbers
from django.http import Http404


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
