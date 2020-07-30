from django.views.generic.base import TemplateView
from users.model.profile import UserProfile
from users.model.settings import *
from users.forms import *
from django.http import HttpResponse, HttpResponseBadRequest
from users.models import User


class UserGeneralChange(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="general.html", request=request)
		return super(UserGeneralChange,self).get(request,*args,**kwargs)


class UserInfoChange(TemplateView):
	template_name = None
	form = None
	profile = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="info.html", request=request)
		return super(UserInfoChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserInfoChange,self).get_context_data(**kwargs)
		context["profile"] = self.profile
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		try:
			self.profile = UserProfile.objects.get(user=request.user)
		except:
			self.profile = UserProfile.objects.create(user=request.user)
		self.form = InfoUserForm(request.POST,instance=self.profile)
		if self.form.is_valid():
			user = self.request.user
			user.first_name = self.form.cleaned_data['first_name']
			user.last_name = self.form.cleaned_data['last_name']
			user.save()
			self.form.save()
			return HttpResponse ('')
		return super(UserInfoChange,self).post(request,*args,**kwargs)


class SettingsNotifyView(TemplateView):
	template_name = None
	form = None
	notify_settings = None

	def get(self,request,*args,**kwargs):
		self.form = SettingsNotifyForm()
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="notifications.html", request=request)
		return super(SettingsNotifyView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(SettingsNotifyView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_settings"] = self.notify_settings
		return context

	def post(self,request,*args,**kwargs):
		try:
			self.notify_settings = UserItemNotifications.objects.get(user=request.user)
		except:
			self.notify_settings = UserItemNotifications.objects.create(user=request.user)
		self.form = SettingsNotifyForm(request.POST,instance=self.notify_settings)
		if self.form.is_valid():
			self.result = self.form.save()
			return HttpResponse ("!")
		return super(SettingsNotifyView,self).post(request,*args,**kwargs)

class UserDesign(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="design.html", request=request)
		return super(UserDesign,self).get(request,*args,**kwargs)
