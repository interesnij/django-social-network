from django.views.generic import ListView
from communities.models import Community, CommunityMembership
from users.models import User


class CommunityMembersView(ListView):
	template_name="members.html"
	model=Community
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityMembersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityMembersView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)
		return membersheeps


class AllCommunities(ListView):
	template_name="all_communities.html"
	model=Community
	paginate_by=15

	def get_queryset(self):
		groups=Community.get_trending_communities()
		return groups
