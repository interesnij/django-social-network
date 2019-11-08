from django.views.generic.base import TemplateView
from communities.models import CommunityCategory, Community, CommunitySubCategory
from django.views import View
from follows.models import CommunityFollow
from notifications.models import CommunityNotification, community_notification_handler


class CommunityCreate(TemplateView):
	template_name="community_add.html"
	form=None
	categories = CommunityCategory.objects.only("id")

	def get(self,request,*args,**kwargs):
		self.form=CommunityForm()
		self.new_community = Community.objects.only('id').last()
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
			return HttpResponseBadRequest()
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


class CommunityMemberCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		new_member = request.user.join_community_with_name(self.community.name)
		self.community.notification_new_member(request.user)
		return HttpResponse("!")

class CommunityMemberDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		request.user.leave_community_with_name(self.community.name)
		return HttpResponse("!")


class GygView(TemplateView):
	template_name="gygyg.html"

	def get(self,request,*args,**kwargs):
		self.new_community = Community.objects.only('id').last()
		self.new_url = self.new_community.pk
		return super(GygView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GygView,self).get_context_data(**kwargs)
		context["new_url"]=self.new_url
		return context
