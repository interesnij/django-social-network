from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.views.generic import ListView
from lists.models import *
from common.templates import get_small_template, get_full_template


class AuthorityListView(ListView, CategoryListMixin):
	template_name, paginate_by = None, 20

	def get(self,request,*args,**kwargs):
		if self.kwargs["slug"] == None:
			self.list = AuthorityList.objects.first()
		else:
			self.list = AuthorityList.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("elect_list/" , "authority_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AuthorityListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.list.get_elects()

	def get_context_data(self,**kwargs):
		from region.models import Region
		context = super(AuthorityListView,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["regions"] = Region.objects.only("pk")
		return context


class RegionAuthorityListView(ListView, CategoryListMixin):
	template_name, paginate_by, districts, okrug = None, 20, None, None

	def get(self,request,*args,**kwargs):
		from region.models import Region

		if self.kwargs["slug"] == None:
			self.list = AuthorityList.objects.first()
		else:
			self.list = AuthorityList.objects.get(slug=self.kwargs["slug"])
		self.region = Region.objects.get(pk=self.kwargs["pk"])
		if self.list.slug == "candidate_municipal":
			from district.models import District2
			self.districts = District2.objects.filter(region=self.region)
		elif self.list.slug == "candidate_duma":
			from okrug.models import Okrug
			self.okrug = Okrug.objects.filter(region=self.region)
		self.template_name = get_full_template("elect_list/region/" , "authority_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(RegionAuthorityListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from region.models import Region
		context = super(RegionAuthorityListView,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["regions"] = Region.objects.only("pk")
		context["region"] = self.region
		context["districts"] = self.districts
		context["okrug"] = self.okrug
		return context

	def get_queryset(self):
		return self.region.get_list_elects(self.list)


class FractionList(ListView, CategoryListMixin):
	template_name, paginate_by = None, 20

	def get(self,request,*args,**kwargs):
		self.list = Fraction.objects.get(slug=self.kwargs["slug"])
		self.template_name = get_full_template("elect_list/", "fraction_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FractionList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FractionList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_elects()


class ElectListsView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_full_template("elect_list/", "all_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(ElectListsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ElectListsView,self).get_context_data(**kwargs)
		context["lists"] = AuthorityList.objects.only("pk")
		return context
