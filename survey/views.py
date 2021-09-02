from django.views.generic import ListView
from survey.models import SurveyList, Survey


class SurveyView(ListView):
	template_name = "survey.html"

	def get_queryset(self):
		return Survey.objects.only("pk")



class LoadSurveyList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
		if self.list.community:
			from common.templates import get_template_community_item, get_template_anon_community_item
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.list, "survey/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.list, "survey/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from common.templates import get_template_user_item, get_template_anon_user_item

			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.list, "survey/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.list, "survey/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadSurveyList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadSurveyList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()
