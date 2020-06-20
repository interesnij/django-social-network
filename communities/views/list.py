from django.views.generic import ListView
from communities.models import Community, CommunityMembership, CommunityCategory
from users.models import User
from common.utils import is_mobile


class CommunityMembersView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityMembersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityMembersView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		import re

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		if self.community.is_private() and not self.request.user.is_member_of_community_with_name(self.name):
			membersheeps = None
			self.template_name = "c_detail/private_community.html"
		else:
			membersheeps = self.community.get_community_with_name_members(self.community.name)
			self.template_name = "c_detail/members.html"
		MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
		if MOBILE_AGENT_RE.match(self.request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return membersheeps


class CommunityFriendsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityFriendsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityFriendsView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		import re

		if self.community.is_private() and not self.request.user.is_member_of_community_with_name(self.community.name):
			frends = None
			self.template_name = "c_detail/private_community.html"
		else:
			frends = self.request.user.get_common_friends_of_community(self.community.pk)
			self.template_name = "c_detail/friends.html"
		MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
		if MOBILE_AGENT_RE.match(self.request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return frends


class AllCommunities(ListView):
	template_name="all_communities.html"
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.template_name = request.user.get_default_template(folder="c_list/", template="all_communities.html", request=request)

	def get_queryset(self):
		groups=Community.get_trending_communities()
		return groups

	def get_context_data(self,**kwargs):
		context=super(AllCommunities,self).get_context_data(**kwargs)
		context["communities_categories"]=CommunityCategory.objects.only("pk")
		return context


class CommunityCategoryView(ListView):
	template_name="cat.html"
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.cat = CommunityCategory.objects.get(pk=self.kwargs["pk"])
		return super(CommunityCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityCategoryView,self).get_context_data(**kwargs)
		context["category"]=self.cat
		context["communities_categories"]=CommunityCategory.objects.only("pk")
		return context

	def get_queryset(self):
		self.cat = CommunityCategory.objects.get(pk=self.kwargs["pk"])
		categories=Community.objects.filter(category__sudcategory = self.cat)
		return categories
