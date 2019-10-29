from django.views.generic import ListView
from users.models import User
from main.models import Item
from communities.models import *
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from communities.forms import CommunityForm


class CommunitiesView(ListView):
	template_name="communities.html"
	model=Community
	paginate_by=10

	def get_queryset(self):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		groups=Community.objects.filter(memberships__user__id=self.user.pk)
		return groups

	def get_context_data(self,**kwargs):
		context=super(CommunitiesView,self).get_context_data(**kwargs)

		return context

class CommunityDetailView(DetailView):
	template_name="community_detail.html"
	model=Community

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.items = Item.objects.filter(community=self.community, is_deleted=False)
		self.membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)
		return super(CommunityDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityDetailView,self).get_context_data(**kwargs)
		context["membersheeps"]=self.membersheeps
		context["items"]=self.items
		return context


class AllCommunities(ListView):
	template_name="all_communities.html"
	model=Community
	paginate_by=10

	def get_queryset(self):
		groups=Community.objects.all()
		return groups


class CommunityCreate(TemplateView):
	template_name="community_add.html"
	form=None
	categories = CommunityCategory.objects.only("id")

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
			Community.create_community(
										name=new_community.name,
										category=new_community.category,
										type=new_community.type,
										creator=request.user)

			if request.is_ajax() :
				return HttpResponse("!")
		else:
			return JsonResponse({'error': True, 'errors': self.form.errors})
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
