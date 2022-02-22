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
	template_name, c, paginate_by, is_user_can_see_good_section, is_user_can_see_good_list, is_user_can_create_goods = None, None, 10, None, None, None

	def get(self,request,*args,**kwargs):
		self.list = GoodList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.c = self.list.community
			if request.user.is_authenticated:
				if request.user.is_staff_of_community(self.c.pk):
					self.get_lists = GoodList.get_community_staff_lists(self.c.pk)
					self.is_user_can_see_good_section = True
					self.is_user_can_create_goods = True
					self.is_user_can_see_good_list = True
					self.template_name = get_template_community_list(self.list, "goods/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
				else:
					self.get_lists = GoodList.get_community_lists(self.c.pk)
					self.is_user_can_see_good_section = self.c.is_user_can_see_good(request.user.pk)
					self.is_user_can_see_good_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_goods = self.list.is_user_can_create_el(request.user.pk)
			elif request.user.is_anonymous:
				self.template_name = get_template_anon_community_list(self.list, "goods/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_good_section = self.c.is_anon_user_can_see_good()
				self.is_user_can_see_good_list = self.list.is_anon_user_can_see_el()
				self.get_lists = GoodList.get_community_lists(self.c.pk)
		else:
			if request.user.is_authenticated:
				creator = self.list.creator
				if request.user.pk == creator.pk:
					self.is_user_can_see_good_section = True
					self.is_user_can_see_good_list = True
					self.is_user_can_create_goods = True
				else:
					self.is_user_can_see_good_section = creator.is_user_can_see_good(request.user.pk)
					self.is_user_can_see_good_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_goods = self.list.is_user_can_create_el(request.user.pk)
				self.template_name = get_template_user_list(self.list, "goods/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "goods/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_good_section = creator.is_anon_user_can_see_good()
				self.is_user_can_see_good_list = self.list.is_anon_user_can_see_el()
		return super(LoadGoodList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadGoodList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.c
		context['is_user_can_see_good_section'] = self.is_user_can_see_good_section
		context['is_user_can_see_good_list'] = self.is_user_can_see_good_list
		context['is_user_can_create_goods'] = self.is_user_can_create_goods
		return context

	def get_queryset(self):
		return self.list.get_items()


class LoadGood(TemplateView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.good = Good.objects.get(uuid=self.kwargs["uuid"])
		self.list = self.good.list

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


class GoodDetail(TemplateView):
	template_name, community, user_form = None, None, None

	def get(self,request,*args,**kwargs):
		self.good = Good.objects.get(pk=self.kwargs["pk"])
		self.list = self.good.list
		self.goods = self.list.get_items()
		if self.good.community:
			self.community = self.good.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.good, "goods/c_good/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.good, "goods/c_good/anon_good.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.good, "goods/u_good/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.good, "goods/u_good/anon_good.html", request.user, request.META['HTTP_USER_AGENT'])
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
