from django.views.generic import ListView
from users.models import User
from main.models import Item
from communities.models import *
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from communities.forms import CommunityForm
from generic.mixins import CategoryListMixin


class CommunitiesView(ListView):
	template_name="communities.html"
	model=Community
	paginate_by=15

	def get_queryset(self):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		groups=Community.objects.filter(memberships__user__id=self.user.pk)
		return groups


class CommunityMembersView(ListView):
	template_name="members.html"
	model=Community
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		if request.user.is_administrator_of_community_with_name(self.community.name):
			self.administrator=True
		else:
			self.administrator=False
		return super(CommunityMembersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityMembersView,self).get_context_data(**kwargs)
		context["administrator"]=self.administrator
		context["community"]=self.community
		return context

	def get_queryset(self):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)
		return membersheeps

class CommunityDetailView(DetailView):
	template_name="community_detail.html"
	model=Community
	

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)[0:5]
		if request.user.is_administrator_of_community_with_name(self.community.name):
			self.administrator=True

		return super(CommunityDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityDetailView,self).get_context_data(**kwargs)
		context["membersheeps"]=self.membersheeps
		context["administrator"]=self.administrator
		return context


class GygView(TemplateView):
	template_name="gygyg.html"

	def get(self,request,*args,**kwargs):
		self.new_community = Community.objects.filter(creator=request.user).last()
		self.new_url = self.new_community.pk
		return super(GygView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GygView,self).get_context_data(**kwargs)
		context["new_url"]=self.new_url
		return context


class CommunityDetailReload(DetailView):
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


class AllCommunities(ListView):
	template_name="all_communities.html"
	model=Community
	paginate_by=15

	def get_queryset(self):
		groups=Community.objects.all()
		return groups


class CommunityCreate(TemplateView):
	template_name="community_add.html"
	form=None
	categories = CommunityCategory.objects.only("id")

	def get(self,request,*args,**kwargs):
		self.form=CommunityForm()
		self.new_community = Community.objects.filter(creator=request.user).last()
		self.new_url = self.new_community.pk + 1
		return super(CommunityCreate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityCreate,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["categories"]=self.categories
		context["new_url"]=self.new_url
		return context

	def post(self,request,*args,**kwargs):
		self.form=CommunityForm(request.POST)
		if self.form.is_valid():
			new_community=self.form.save(commit=False)
			Community.create_community(
										name=new_community.name,
										category=new_community.category,
										type=new_community.type,
										creator=request.user
										)
			if request.is_ajax() :
				return HttpResponse("!")
		else:
			return JsonResponse({'errors': self.form.errors})
		return super(CommunityCreate,self).get(request,*args,**kwargs)


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


class CommunityItemView(CategoryListMixin, TemplateView):
    model=Item
    template_name="community/item.html"

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
	template_name="community/list.html"
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
		communities = Item.objects.filter(community=self.community,is_deleted=False)
		return communities

	def get_context_data(self, **kwargs):
		context = super(CommunityListView, self).get_context_data(**kwargs)
		context['object'] = self.fixed
		return context
