from django.views.generic import ListView
from communities.models import Community, CommunityCategory
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from communities.forms import CommunityForm, GeneralCommunityForm
from django.views import View


class CommunityGeneralChange(TemplateView):
	template_name = "manage/general.html"
	form=None
	categories = CommunityCategory.objects.only("id")

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=GeneralCommunityForm()
		return super(CommunityGeneralChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityGeneralChange,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["community"]=self.community
		context["categories"]=self.categories
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=GeneralCommunityForm(request.POST, request.FILES, instance=self.community)
		if self.form.is_valid() and request.user.is_authenticated and request.user.is_administrator_of_community_with_name(self.community.name):
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(CommunityGeneralChange,self).post(request,*args,**kwargs)
