from django.views.generic.base import TemplateView
from communities.models import *
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from communities.forms import CommunityForm
from gallery.models import Album
from users.models import User
from django.shortcuts import render


class UserCreateCommunityWindow(TemplateView):
	template_name = "manage/create_community.html"

	def get(self,request,*args,**kwargs):
		return super(UserCreateCommunityWindow,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCreateCommunityWindow,self).get_context_data(**kwargs)
		context["form"] = CommunityForm()
		context["categories"] = CommunityCategory.objects.only("id")
		return context


class CommunityCreate(TemplateView):
	template_name="community_add.html"

	def get(self,request,*args,**kwargs):
		self.form=CommunityForm()
		return super(CommunityCreate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityCreate,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["categories"]=self.categories
		return context

	def post(self,request,*args,**kwargs):
		self.form=CommunityForm(request.POST)
		if self.form.is_valid():
			new_community=self.form.save(commit=False)
			community = Community.create_community(name=new_community.name, category=new_community.category, type=new_community.type, creator=request.user)
			membersheeps=[request.user,]
			return render(request, 'c_detail/admin_community.html',{'community': community, 'membersheeps': membersheeps, 'user': request.user})
		else:
			HttpResponseBadRequest()


class CommunitiesCatsView(TemplateView):
	template_name="communities_cats.html"
	categ = None

	def get(self,request,*args,**kwargs):
		self.categ = CommunitySubCategory.objects.filter(sudcategory__order=self.kwargs["order"])
		return super(CommunitiesCatsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunitiesCatsView,self).get_context_data(**kwargs)
		context["categ"]=self.categ
		return context


class CommunityMemberCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		new_member = request.user.join_community_with_name(self.community.name)
		return HttpResponse("!")
class CommunityMemberDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		request.user.leave_community_with_name(self.community.name)
		return HttpResponse("!")


class CommunityAdminCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			new_admin = self.community.add_administrator(self.user)
			return HttpResponse("!")
		else:
			return HttpResponse("!")
class CommunityAdminDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			new_admin = self.community.remove_administrator(self.user)
		else:
			return HttpResponse("!")
		return HttpResponse("!")


class CommunityModerCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			new_moderator = self.community.add_moderator(self.user)
		else:
			return HttpResponse("!")
		return HttpResponse("!")
class CommunityModerDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			new_moderator = self.community.remove_moderator(self.user)
		else:
			return HttpResponse("!")
		return HttpResponse("!")

class CommunityEditorCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			new_editor = self.community.add_editor(self.user)
		else:
			return HttpResponse("!")
		return HttpResponse("!")
class CommunityEditorDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			new_editor = self.community.remove_editor(self.user)
		else:
			return HttpResponse("!")
		return HttpResponse("!")

class CommunityAdvertiserCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			new_advertiser = self.community.add_advertiser(self.user)
		else:
			return HttpResponse("!")
		return HttpResponse("!")
class CommunityAdvertiserDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			new_advertiser = self.community.remove_advertiser(self.user)
		else:
			return HttpResponse("!")
		return HttpResponse("!")
