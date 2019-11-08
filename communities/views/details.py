from generic.mixins import EmojiListMixin, CommunityMemdersMixin
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from main.models import Item
from communities.models import Community, CommunityMembership
from django.views.generic.detail import DetailView



class CommunityItemView(EmojiListMixin, TemplateView):
    model=Item
    template_name="detail/item.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.item.views += 1
        self.item.save()
        return super(CommunityItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityItemView,self).get_context_data(**kwargs)
        context["object"]=self.item
        return context


class CommunityListView(ListView):
	template_name="detail/list.html"
	model=Item
	paginate_by=15

	def get(self,request,*args,**kwargs):
		try:
			self.fixed = Item.objects.get(community=self.community, is_fixed=True)
		except:
			self.fixed = None
		return super(CommunityListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		self.community=Community.objects.get(pk=self.kwargs["pk"])
		communities = self.community.get_posts()
		return communities

	def get_context_data(self, **kwargs):
		context = super(CommunityListView, self).get_context_data(**kwargs)
		context['object'] = self.fixed
		return context


class CommunityDetailView(DetailView, CommunityMemdersMixin):
	template_name = "community_detail.html"
	model = Community

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)[0:5]
		return super(CommunityDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityDetailView,self).get_context_data(**kwargs)
		context["membersheeps"]=self.membersheeps
		return context


class CommunityDetailReload(DetailView, CommunityMemdersMixin):
	template_name="detail_reload.html"
	model=Community

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)[0:5]
		return super(CommunityDetailReload,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityDetailReload,self).get_context_data(**kwargs)
		context["membersheeps"]=self.membersheeps
		return context
