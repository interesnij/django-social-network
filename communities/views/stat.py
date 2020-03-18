from django.views.generic.base import TemplateView
from communities.models import Community
from stst.models import CommunityNumbers


class CommunityCoberturaMonth(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="community_stat/", template="cobertura_month.html", request=request)
		self._months = CommunityNumbers.objects.values('created__month').distinct()
		self.months = [i['created__month'] for i in self._months]
		self.month_query = CommunityNumbers.objects.filter(community=self.community.pk, created__month=self.months[0]).distinct("user").values('platform')
		self.phone_count = self.month_query.filter(platform=1)
		self.comp_count = self.month_query.filter(platform=0)
		self.phone = len(self.phone_count)/len(self.month_query)*100
		self.comp = len(self.comp_count)/len(self.month_query)*100
		return super(CommunityCoberturaMonth,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCoberturaMonth,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["phone"] = round(self.phone)
		context["comp"] = round(self.comp)
		context["months"] = self.months[:5 ]
		context["month"] = self.months[0]
		context["month_views"] = len(self.month_query)
		return context

class CommunityCoberturaDay(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="community_stat/", template="cobertura_day.html", request=request)
		self._days = CommunityNumbers.objects.values('created__day').distinct()[0:10]
		self.__days = [i['created__day'] for i in self._days]
		self.days = [a for CommunityNumbers.objects.filter(community=community_id, created__day=i).distinct("user").values('platform').count() in self.__days]
		self.days_query = CommunityNumbers.objects.filter(community=self.community.pk, created__day=self.days[0]).distinct("user").values('platform')
		self.phone_count = self.days_query.filter(platform=1)
		self.comp_count = self.days_query.filter(platform=0)
		self.phone = len(self.phone_count)/len(self.days_query)*100
		self.comp = len(self.comp_count)/len(self.days_query)*100
		return super(CommunityCoberturaDay,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCoberturaDay,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["phone"] = round(self.phone)
		context["comp"] = round(self.comp)
		context["days"] = self.days
		return context
