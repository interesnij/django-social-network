from django.views.generic.base import TemplateView
from communities.models import *
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from communities.forms import CommunityForm
from gallery.models import Album
from users.models import User
from django.shortcuts import render
from django.http import Http404


class UserCreateCommunityWindow(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = "manage/create_community.html"
		else:
			self.template_name = "about.html"
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
		if self.form.is_valid() and request.is_ajax():
			new_community=self.form.save(commit=False)
			community = Community.create_community(name=new_community.name, category=new_community.category, type=new_community.type, creator=request.user)
			membersheeps = [request.user,]
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
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			new_member = request.user.join_community_with_name(self.community.name)
			return HttpResponse()
		else:
			raise Http404
class CommunityMemberDelete(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			request.user.leave_community_with_name(self.community.name)
			return HttpResponse()
		else:
			raise Http404

class CommunityManageMemberCreate(View):
	def get(self,request,*args,**kwargs):
		community = Community.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax():
			new_member = user.join_community_with_name(community.name)
			return HttpResponse()
		else:
			raise Http404
class CommunityManageMemberDelete(View):
	def get(self,request,*args,**kwargs):
		community = Community.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax():
			user.leave_community_with_name(community.name)
			return HttpResponse()
		else:
			raise Http404

class CommunityAdminCreate(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.is_administrator_of_community_with_name(self.community.name):
			new_admin = self.community.add_administrator(self.user)
			return HttpResponse("!")
		else:
			raise Http404
class CommunityAdminDelete(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.is_administrator_of_community_with_name(self.community.name):
			new_admin = self.community.remove_administrator(self.user)
			return HttpResponse("!")
		else:
			raise Http404

class CommunityModerCreate(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.is_administrator_of_community_with_name(self.community.name):
			new_moderator = self.community.add_moderator(self.user)
			return HttpResponse("!")
		else:
			raise Http404
class CommunityModerDelete(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.is_administrator_of_community_with_name(self.community.name):
			new_moderator = self.community.remove_moderator(self.user)
			return HttpResponse("!")
		else:
			raise Http404

class CommunityEditorCreate(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.is_administrator_of_community_with_name(self.community.name):
			new_editor = self.community.add_editor(self.user)
			return HttpResponse("!")
		else:
			raise Http404
class CommunityEditorDelete(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.is_administrator_of_community_with_name(self.community.name):
			new_editor = self.community.remove_editor(self.user)
			return HttpResponse("!")
		else:
			raise Http404

class CommunityAdvertiserCreate(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.is_administrator_of_community_with_name(self.community.name):
			new_advertiser = self.community.add_advertiser(self.user)
			return HttpResponse("!")
		else:
			raise Http404
class CommunityAdvertiserDelete(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.is_administrator_of_community_with_name(self.community.name):
			new_advertiser = self.community.remove_advertiser(self.user)
			return HttpResponse("!")
		else:
			raise Http404
