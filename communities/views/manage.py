from django.views.generic import ListView
from communities.models import *
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View
from communities.forms import *
from users.models import User


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


class CommunityNotifyView(TemplateView):
	template_name = "manage/notifications_settings.html"
	form=None
	notify_settings=None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=CommunityNotifyForm(instance=self.community)
		return super(CommunityNotifyView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityNotifyView,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["notify_settings"]=self.notify_settings
		context["community"]=self.community
		return context

	def post(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		try:
			self.notify_settings=CommunityNotificationsSettings.objects.get(community=self.community)
		except:
			self.notify_settings = None
		if not self.notify_settings:
			self.user.notify_settings = CommunityNotificationsSettings.objects.create(community=self.community)
		self.form=CommunityNotifyForm(request.POST,instance=self.notify_settings)
		if self.form.is_valid() and request.user.is_authenticated and request.user.is_administrator_of_community_with_name(self.community.name):
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(CommunityNotifyView,self).post(request,*args,**kwargs)


class CommunityPrivateView(TemplateView):
	template_name = "manage/private_settings.html"
	form=None
	private_settings=None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=CommunityPrivateForm(instance=self.community)
		return super(CommunityPrivateView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityPrivateView,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["community"]=self.community
		return context

	def post(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_settings=CommunityPrivateSettings.objects.get(community=self.community)
		except:
			self.private_settings = None
		if not self.private_settings:
			self.user.private_settings = CommunityPrivateSettings.objects.create(community=self.community)
		self.form=CommunityPrivateForm(request.POST,instance=self.private_settings)
		if self.form.is_valid() and request.user.is_authenticated and request.user.is_administrator_of_community_with_name(self.community.name):
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(CommunityPrivateView,self).post(request,*args,**kwargs)


class CommunityAdminView(ListView):
	template_name="manage/admins.html"
	model=User
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityAdminView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityAdminView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		admins=self.community.get_community_with_name_administrators(self.community.name)
		return admins


class CommunityModersView(ListView):
	template_name="manage/moders.html"
	model=User
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityModersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityModersView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		moders=self.community.get_community_with_name_moderators(self.community.name)
		return moders
