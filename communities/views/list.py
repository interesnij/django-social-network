from django.views.generic import ListView
from communities.models import Community, CommunityMembership
from users.models import User


class CommunityMembersView(ListView):
	template_name="members.html"
	model=Community
	paginate_by=30

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityMembersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityMembersView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		membersheeps=self.community.get_community_with_name_members(self.community.name)
		return membersheeps


class CommunityFriendsView(ListView):
	template_name="friends.html"
	model=Community
	paginate_by=30

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityFriendsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityFriendsView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		friends=self.request.user.get_common_friends_of_community(self.community.pk)
		return friends


class AllCommunities(ListView):
	template_name="all_communities.html"
	model=Community
	paginate_by=30

	def get_queryset(self):
		groups=Community.get_trending_communities()
		return groups
