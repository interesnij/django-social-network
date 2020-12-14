from django.views.generic.base import TemplateView
from stst.models import UserNumbers
from users.models import User
from common.template.user import get_settings_template


class UserCoberturaYear(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.views, self.sities, self.years, self.template_name, pk = [], [], UserNumbers.objects.dates('created', 'year')[0:10], get_settings_template("users/user_stat/cobertura_year.html", request.user, request.META['HTTP_USER_AGENT']), request.user.pk
		for i in self.years:
			view = UserNumbers.objects.filter(created__year=i.year, target=pk).distinct("target").count()
			self.views += [view]
		current_views = UserNumbers.objects.filter(created__year=self.years[0].year, target=pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано"]

		return super(UserCoberturaYear,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCoberturaYear,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["years"] = self.years
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class UserCoberturaMonth(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.views, self.sities, self.months, self.template_name, pk = [], [], UserNumbers.objects.dates('created', 'month')[0:10], get_settings_template("users/user_stat/cobertura_month.html", request.user, request.META['HTTP_USER_AGENT']), request.user.pk
		for i in self.months:
			view = UserNumbers.objects.filter(created__month=i.month, target=pk).distinct("target").count()
			self.views += [view]

		current_views = UserNumbers.objects.filter(created__month=self.months[0].month, target=pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано"]
		return super(UserCoberturaMonth,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCoberturaMonth,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["months"] = self.months
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class UserCoberturaWeek(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		import datetime

		self.range, self.views, self.sities, self.weeks, self.template_name, pk = [], [], [], UserNumbers.objects.dates('created', 'week')[0:10], get_settings_template("users/user_stat/cobertura_week.html", request.user, request.META['HTTP_USER_AGENT']), request.user.pk
		for i in self.weeks:
			days = [i.day, i.day + 1, i.day + 2, i.day + 3, i.day + 4, i.day + 5, i.day + 6]
			view = UserNumbers.objects.filter(created__day__in=days, target=pk).distinct("target").count()
			i6 = i + datetime.timedelta(days=7)
			self.range += [str(i.strftime('%d.%m')) + " - " + str(i6.strftime('%d.%m'))]
			self.views += [view ]
		dss = [self.weeks[0].day, self.weeks[0].day + 1, self.weeks[0].day + 2, self.weeks[0].day + 3, self.weeks[0].day + 4, self.weeks[0].day + 5, self.weeks[0].day + 6]
		current_views = UserNumbers.objects.filter(created__day__in=dss, target=pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано"]
		return super(UserCoberturaWeek,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCoberturaWeek,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["weeks"] = self.weeks
		context["range"] = self.range
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context

class UserCoberturaDay(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.views, self.sities, self.days, self.template_name, pk = [], [], UserNumbers.objects.dates('created', 'day')[0:10], get_settings_template("users/user_stat/cobertura_day.html", request.user, request.META['HTTP_USER_AGENT']), request.user.pk
		for i in self.days:
			view = UserNumbers.objects.filter(created__day=i.day, target=pk).distinct("target").count()
			self.views += [view]
		current_views = UserNumbers.objects.filter(created__day=self.days[0].day, target=pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано"]
		return super(UserCoberturaDay,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCoberturaDay,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["days"] = self.days
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class UserTrafficYear(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.views, self.un_views, self.sities, self.years, self.template_name, pk = [], [], [], UserNumbers.objects.dates('created', 'year')[0:10], get_settings_template("users/user_stat/traffic_year.html", request.user, request.META['HTTP_USER_AGENT']), request.user.pk
		for i in self.years:
			view = UserNumbers.objects.filter(created__year=i.year, target=pk).count()
			self.views += [view]
		for i in self.years:
			view = UserNumbers.objects.filter(created__year=i.year, target=pk).distinct("target").count()
			self.un_views += [view]

		current_views = UserNumbers.objects.filter(created__year=self.years[0].year, target=pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано"]
		return super(UserTrafficYear,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserTrafficYear,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["years"] = self.years
		context["un_views"] = self.un_views
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class UserTrafficMonth(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.views, self.un_views, self.sities, self.months, self.template_name, pk = [], [], [], UserNumbers.objects.dates('created', 'month')[0:10], get_settings_template("users/user_stat/traffic_month.html", request.user, request.META['HTTP_USER_AGENT']), request.user.pk
		for i in self.months:
			view = UserNumbers.objects.filter(created__month=i.month, target=pk).count()
			self.views += [view]
		for i in self.months:
			view = UserNumbers.objects.filter(created__month=i.month, target=pk).distinct("target").count()
			self.un_views += [view]

		current_views = UserNumbers.objects.filter(created__month=self.months[0].month, target=pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано"]
		return super(UserTrafficMonth,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserTrafficMonth,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["months"] = self.months
		context["un_views"] = self.un_views
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context


class UserTrafficWeek(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		import datetime

		self.views, self.range, self.un_views, self.sities, self.weeks, self.template_name, pk = [], [], [], [], UserNumbers.objects.dates('created', 'week')[0:10], get_settings_template("users/user_stat/traffic_week.html", request.user, request.META['HTTP_USER_AGENT']), request.user.pk
		for i in self.weeks:
			days = [i.day, i.day + 1, i.day + 2, i.day + 3, i.day + 4, i.day + 5, i.day + 6]
			view = UserNumbers.objects.filter(created__day__in=days, target=pk).count()
			i6 = i + datetime.timedelta(days=7)
			self.range += [str(i.strftime('%d.%m')) + " - " + str(i6.strftime('%d.%m'))]
			self.views += [view ]
		for i in self.weeks:
			days = [i.day, i.day + 1, i.day + 2, i.day + 3, i.day + 4, i.day + 5, i.day + 6]
			view = UserNumbers.objects.filter(created__day__in=days, target=pk).distinct("target").count()
			self.un_views += [view]

		dss = [self.weeks[0].day, self.weeks[0].day + 1, self.weeks[0].day + 2, self.weeks[0].day + 3, self.weeks[0].day + 4, self.weeks[0].day + 5, self.weeks[0].day + 6]
		current_views = UserNumbers.objects.filter(created__day__in=dss, target=pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано"]
		return super(UserTrafficWeek,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserTrafficWeek,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["un_views"] = self.un_views
		context["views"] = self.views
		context["range"] = self.range
		context["sities"] = set(self.sities)
		return context


class UserTrafficDay(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.views, self.un_views, self.sities, self.weeks, self.template_name, pk = [], [], [], UserNumbers.objects.dates('created', 'day')[0:10], get_settings_template("users/user_stat/traffic_day.html", request.user, request.META['HTTP_USER_AGENT']), request.user.pk
		for i in self.days:
			view = UserNumbers.objects.filter(created__day=i.day, target=pk).count()
			self.views += [view]
		for i in self.days:
			view = UserNumbers.objects.filter(created__day=i.day, target=pk).distinct("target").count()
			self.un_views += [view]

		current_views = UserNumbers.objects.filter(created__day=self.days[0].day, target=pk).values('target').distinct()
		user_ids = [use['target'] for use in current_views]
		users = User.objects.filter(id__in=user_ids)
		for user in users:
			try:
				sity = user.get_last_location().city_ru
				self.sities += [sity]
			except:
				self.sities += ["Местоположение не указано"]
		return super(UserTrafficDay,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserTrafficDay,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["days"] = self.days
		context["un_views"] = self.un_views
		context["views"] = self.views
		context["sities"] = set(self.sities)
		return context
