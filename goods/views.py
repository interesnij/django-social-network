from goods.models import Good, GoodList
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
							)


class GoodsView(ListView):
	template_name = "goods.html"

	def get_queryset(self):
		return Good.objects.only("pk")


class LoadGoodList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = GoodList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_list(self.list, "goods/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_list(self.list, "goods/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_list(self.list, "goods/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_list(self.list, "goods/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadGoodList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadGoodList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()


class LoadGood(TemplateView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.good = Good.objects.get(uuid=self.kwargs["uuid"])
		self.list = self.good.list

		if self.list.community:
			if request.user.is_authenticated:
				if request.user.is_administrator_of_community(self.list.pk):
					self.goods = self.list.get_staff_items()
				else:
					self.goods = self.list.get_items()
			else:
				self.goods = self.list.get_items()
		else:
			if request.user.pk == self.list.creator.pk:
				self.goods = self.list.get_staff_items()
			else:
				self.goods = self.list.get_items()

		if self.good.community:
			self.community = self.good.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.good, "goods/user/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.good, "goods/user/anon_good.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.good, "goods/user/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.good, "goods/user/anon_good.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(LoadGood,self).get_context_data(**kwargs)
		c["object"] = self.good
		c["community"] = self.community
		if self.goods.filter(order=self.good.order + 1).exists():
			c["next"] = self.goods.filter(order=self.good.order + 1)[0]
		if self.goods.filter(order=self.good.order - 1).exists():
			c["prev"] = self.goods.filter(order=self.good.order - 1)[0]
		return c


class GoodCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_comments, get_template_community_comments

		self.good = Good.objects.get(pk=self.kwargs["pk"])
		if not request.is_ajax() or not self.good.comments_enabled:
			raise Http404
		if self.good.community:
			self.template_name = get_template_user_comments(self.good, "goods/c_good_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_user_comments(self.good, "goods/u_good_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodCommentList,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(GoodCommentList, self).get_context_data(**kwargs)
		context['parent'] = self.good
		return context

	def get_queryset(self):
		return self.good.get_comments()


class GoodDetail(TemplateView):
	template_name, community, user_form = None, None, None

	def get(self,request,*args,**kwargs):
		self.good = Good.objects.get(pk=self.kwargs["pk"])
		self.list = self.good.list
		if self.good.community:
			self.community = self.good.community
			if request.user.is_administrator_of_community(self.community.pk):
				self.goods = self.list.get_staff_items()
			else:
				self.goods = self.list.get_items()
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.good, "good/c_good/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.good, "good/c_good/anon_good.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.pk == self.good.creator.pk:
				self.goods = self.list.get_staff_items()
			else:
				self.goods = self.list.get_items()
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.good, "good/u_good/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.good, "good/u_good/anon_good.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GoodDetail,self).get_context_data(**kwargs)
		context["object"] = self.good
		context["list"] = self.list
		if self.goods.filter(order=self.good.order + 1).exists():
			context["next"] = self.goods.filter(order=self.good.order + 1)[0]
		if self.goods.filter(order=self.good.order - 1).exists():
			context["prev"] = self.goods.filter(order=self.good.order - 1)[0]
		context["community"] = self.community
		return context
