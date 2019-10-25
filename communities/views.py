from django.views.generic import ListView
from users.models import User
from communities.models import Community
from django.views.generic.detail import DetailView



class CommunitiesView(ListView):
	template_name="communities.html"
	model=Community
	paginate_by=10

	def get_queryset(self):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        groups=Community.objects.filter(starrers=self.user)
        return groups

	def get_context_data(self,**kwargs):
		context=super(CommunitiesView,self).get_context_data(**kwargs)

		return context

class CommunityDetailView(DetailView):
	template_name="community_detail.html"
	model=Community


class AllCommunities(ListView):
    template_name="all_communities.html"
    model=Community
	paginate_by=10

	def get_queryset(self):
        groups=Community.objects.all()
        return groups
