from django.views.generic import ListView
from communities.models import Community, CommunityCategory
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from communities.forms import GeneralCommunityForm, CoverCommunityForm, AvatarCommunityForm, CatCommunityForm
from django.views import View


class CommunityGeneralChange(TemplateView):
	template_name = "manage/general.html"
	form=None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=GeneralCommunityForm()
		return super(CommunityGeneralChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityGeneralChange,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["community"]=self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=GeneralCommunityForm(request.POST, instance=self.community)
		if self.form.is_valid() and request.user.is_authenticated and request.user.is_administrator_of_community_with_name(self.community.name):
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(CommunityGeneralChange,self).post(request,*args,**kwargs)


class CommunityAvatarChange(TemplateView):
	template_name = "manage/avatar.html"
	form=None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=AvatarCommunityForm()
		return super(CommunityAvatarChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityAvatarChange,self).get_context_data(**kwargs)
		context["community"]=self.community
		context["form"]=self.form
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=AvatarCommunityForm(request.POST,request.FILES, instance=self.community)
		if self.form.is_valid():
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(CommunityAvatarChange,self).post(request,*args,**kwargs)


class CommunityCoverChange(TemplateView):
	template_name = "manage/cover.html"
	form=None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=CoverCommunityForm()
		return super(CommunityCoverChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityCoverChange,self).get_context_data(**kwargs)
		context["community"]=self.community
		context["form"]=self.form
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=CoverCommunityForm(request.POST,request.FILES, instance=self.community)
		if self.form.is_valid():
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(CommunityCoverChange,self).post(request,*args,**kwargs)


class CommunityCatChange(TemplateView):
	template_name = "manage/category.html"
	form=None
	categories = CommunityCategory.objects.only("id")

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=CatCommunityForm()
		return super(CommunityCatChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityCatChange,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["community"]=self.community
		context["categories"]=self.categories
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=CatCommunityForm(request.POST, instance=self.community)
		if self.form.is_valid() and request.user.is_authenticated and request.user.is_administrator_of_community_with_name(self.community.name):
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(CommunityCatChange,self).post(request,*args,**kwargs)
