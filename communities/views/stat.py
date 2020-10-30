from django.views.generic.base import TemplateView
from communities.models import Community
from stst.models import CommunityNumbers
from users.models import User


class CommunityCoberturaYear(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="communities/stat/", template="cobertura_year.html", request=request)
		self.years = CommunityNumbers.objects.dates('created', 'year')[0:10]
		self.views = []
		self.sities = []
		for i in self.years:
			view = CommunityNumbers.objects.filter(created__year=i.year, community=self.community.pk).distinct("user").count()
			self.views += [view]
		current_views = CommunityNumbers.objects.filter(created__year=self.years[0].year, community=self.community.pk).values('user').distinct()
		user_ids = [use['user'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]

		return super(CommunityCoberturaYear,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCoberturaYear,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["years"] = self.years
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class CommunityCoberturaMonth(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="communities/stat/", template="cobertura_month.html", request=request)
		self.months = CommunityNumbers.objects.dates('created', 'month')[0:10]
		self.views = []
		self.sities = []
		for i in self.months:
			view = CommunityNumbers.objects.filter(created__month=i.month, community=self.community.pk).distinct("user").count()
			self.views += [view]

		current_views = CommunityNumbers.objects.filter(created__month=self.months[0].month, community=self.community.pk).values('user').distinct()
		user_ids = [use['user'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(CommunityCoberturaMonth,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCoberturaMonth,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["months"] = self.months
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class CommunityCoberturaWeek(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		import datetime
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="communities/stat/", template="cobertura_week.html", request=request)
		self.weeks = CommunityNumbers.objects.dates('created', 'week')[0:10]
		self.range = []
		self.views = []
		self.sities = []
		for i in self.weeks:
			days = [i.day, i.day + 1, i.day + 2, i.day + 3, i.day + 4, i.day + 5, i.day + 6]
			view = CommunityNumbers.objects.filter(created__day__in=days, community=self.community.pk).distinct("user").count()
			i6 = i + datetime.timedelta(days=7)
			self.range += [str(i.strftime('%d.%m.%Y')) + " - " + str(i6.strftime('%d.%m.%Y'))]
			self.views += [view ]
		dss = [self.weeks[0].day, self.weeks[0].day + 1, self.weeks[0].day + 2, self.weeks[0].day + 3, self.weeks[0].day + 4, self.weeks[0].day + 5, self.weeks[0].day + 6]
		current_views = CommunityNumbers.objects.filter(created__day__in=dss, community=self.community.pk).values('user').distinct()
		user_ids = [use['user'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(CommunityCoberturaWeek,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCoberturaWeek,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["weeks"] = self.weeks
		context["range"] = self.range
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context

class CommunityCoberturaDay(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="communities/stat/", template="cobertura_day.html", request=request)
		self.days = CommunityNumbers.objects.dates('created', 'day')[0:10]
		self.views = []
		self.sities = []
		for i in self.days:
			view = CommunityNumbers.objects.filter(created__day=i.day, community=self.community.pk).distinct("user").count()
			self.views += [view]
		current_views = CommunityNumbers.objects.filter(created__day=self.days[0].day, community=self.community.pk).values('user').distinct()
		user_ids = [use['user'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(CommunityCoberturaDay,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCoberturaDay,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["days"] = self.days
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class CommunityTrafficYear(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="communities/stat/", template="traffic_year.html", request=request)
		self.years = CommunityNumbers.objects.dates('created', 'year')[0:10]
		self.views = []
		self.un_views = []
		self.sities = []
		for i in self.years:
			view = CommunityNumbers.objects.filter(created__year=i.year, community=self.community.pk).count()
			self.views += [view]
		for i in self.years:
			view = CommunityNumbers.objects.filter(created__year=i.year, community=self.community.pk).distinct("user").count()
			self.un_views += [view]

		current_views = CommunityNumbers.objects.filter(created__year=self.years[0].year, community=self.community.pk).values('user').distinct()
		user_ids = [use['user'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(CommunityTrafficYear,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityTrafficYear,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["years"] = self.years
		context["un_views"] = self.un_views
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class CommunityTrafficMonth(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="communities/stat/", template="traffic_month.html", request=request)
		self.months = CommunityNumbers.objects.dates('created', 'month')[0:10]
		self.views = []
		self.un_views = []
		self.sities = []
		for i in self.months:
			view = CommunityNumbers.objects.filter(created__month=i.month, community=self.community.pk).count()
			self.views += [view]
		for i in self.months:
			view = CommunityNumbers.objects.filter(created__month=i.month, community=self.community.pk).distinct("user").count()
			self.un_views += [view]

		current_views = CommunityNumbers.objects.filter(created__month=self.months[0].month, community=self.community.pk).values('user').distinct()
		user_ids = [use['user'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(CommunityTrafficMonth,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityTrafficMonth,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["months"] = self.months
		context["un_views"] = self.un_views
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class CommunityTrafficWeek(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		import datetime
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="communities/stat/", template="traffic_week.html", request=request)
		self.weeks = CommunityNumbers.objects.dates('created', 'week')[0:10]
		self.views = []
		self.un_views = []
		self.range = []
		self.sities = []
		for i in self.weeks:
			days = [i.day, i.day + 1, i.day + 2, i.day + 3, i.day + 4, i.day + 5, i.day + 6]
			view = CommunityNumbers.objects.filter(created__day__in=days, community=self.community.pk).count()
			i6 = i + datetime.timedelta(days=7)
			self.range += [str(i.strftime('%d.%m.%Y')) + " - " + str(i6.strftime('%d.%m.%Y'))]
			self.views += [view ]
		for i in self.weeks:
			days = [i.day, i.day + 1, i.day + 2, i.day + 3, i.day + 4, i.day + 5, i.day + 6]
			view = CommunityNumbers.objects.filter(created__day__in=days, community=self.community.pk).distinct("user").count()
			self.un_views += [view]

		dss = [self.weeks[0].day, self.weeks[0].day + 1, self.weeks[0].day + 2, self.weeks[0].day + 3, self.weeks[0].day + 4, self.weeks[0].day + 5, self.weeks[0].day + 6]
		current_views = CommunityNumbers.objects.filter(created__day__in=dss, community=self.community.pk).values('user').distinct()
		user_ids = [use['user'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(CommunityTrafficWeek,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityTrafficWeek,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["un_views"] = self.un_views
		context["views"] = self.views
		context["range"] = self.range
		context["sities"] = set(self.sities)
		return context


class CommunityTrafficDay(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_manage_template(folder="communities/stat/", template="traffic_day.html", request=request)
		self.days = CommunityNumbers.objects.dates('created', 'day')[0:10]
		self.views = []
		self.un_views = []
		self.sities = []
		for i in self.days:
			view = CommunityNumbers.objects.filter(created__day=i.day, community=self.community.pk).count()
			self.views += [view]
		for i in self.days:
			view = CommunityNumbers.objects.filter(created__day=i.day, community=self.community.pk).distinct("user").count()
			self.un_views += [view]

		current_views = CommunityNumbers.objects.filter(created__day=self.days[0].day, community=self.community.pk).values('user').distinct()
		user_ids = [use['user'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано",]
		return super(CommunityTrafficDay,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityTrafficDay,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["days"] = self.days
		context["un_views"] = self.un_views
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context
