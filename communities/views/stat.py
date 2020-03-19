from django.views.generic.base import TemplateView
from communities.models import Community
from stst.models import CommunityNumbers


class CommunityCoberturaMonth(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="community_stat/", template="cobertura_month.html", request=request)
		self._months = CommunityNumbers.objects.values('created__month').distinct()[0:10]
		self.months = [i['created__month'] for i in self._months]
		self.views = []
		for i in self.months:
			view = CommunityNumbers.objects.filter(created__month=i, community=self.community.pk).distinct("user").count()
			self.views += [view,]
		return super(CommunityCoberturaMonth,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCoberturaMonth,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["months"] = self.months
		context["views"] = self.views
		return context

class CommunityCoberturaDay(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="community_stat/", template="cobertura_day.html", request=request)
		self._days = CommunityNumbers.objects.values('created__day').distinct()[0:10]
		self.days = [i['created__day'] for i in self._days]
		self.views = []
		for i in self.days:
			view = CommunityNumbers.objects.filter(created__day=i, community=self.community.pk).distinct("user").count()
			self.views += [view,]
		return super(CommunityCoberturaDay,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCoberturaDay,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["days"] = self.days
		context["views"] = self.views
		return context



class CommunityTrafficMonth(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="community_stat/", template="traffic_month.html", request=request)
		self.months = CommunityNumbers.objects.dates('created', 'month')[0:10]
		self.views = []
		for i in self.months:
			view = CommunityNumbers.objects.filter(created__month=i[2], community=self.community.pk).count()
			self.views += [view,]
		self.un_views = self.views.distinct("user")
		return super(CommunityTrafficMonth,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityTrafficMonth,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["months"] = self.months
		context["un_views"] = self.un_views
		context["views"] = self.views
		return context

class CommunityTrafficDay(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="community_stat/", template="traffic_day.html", request=request)
		self.days = CommunityNumbers.objects.dates('created', 'day')[0:10]
		self.views = []
		self.un_views = []
		for i in self.days:
			view = CommunityNumbers.objects.filter(created__day=i.day, community=self.community.pk).count()
			self.views += [view,]
		for i in self.days:
			view = CommunityNumbers.objects.filter(created__day=i.day, community=self.community.pk).distinct("user").count()
			self.un_views += [view,]
		return super(CommunityTrafficDay,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityTrafficDay,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["days"] = self.days
		context["un_views"] = self.un_views
		context["views"] = self.views
		return context
