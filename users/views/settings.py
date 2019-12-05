from django.views.generic.base import TemplateView
from users.models import (
                            User,
                            UserProfile,
                            UserPrivateSettings,
                            UserNotificationsSettings
                        )
from users.forms import (
                            GeneralUserForm,
                            AboutUserForm,
                            SettingsPrivateForm,
                            SettingsNotifyForm
                        )

from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View



class UserGeneralChange(TemplateView):
	template_name = "settings/user_general_form.html"
	form=None
	profile=None

	def get(self,request,*args,**kwargs):
		self.user=request.user
		self.form=GeneralUserForm(instance=self.user)
		return super(UserGeneralChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserGeneralChange,self).get_context_data(**kwargs)
		context["profile"]=self.profile
		context["form"]=self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user=request.user
		try:
			self.profile=UserProfile.objects.get(user=request.user)
		except:
			self.profile = None
		if not self.profile:
			self.user.profile = UserProfile.objects.create(user=request.user)
		self.form=GeneralUserForm(request.POST,instance=self.user.profile)
		if self.form.is_valid():
			user = self.request.user
			user.first_name = self.form.cleaned_data['first_name']
			user.last_name = self.form.cleaned_data['last_name']
			user.save()
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(UserGeneralChange,self).post(request,*args,**kwargs)


class UserAboutChange(TemplateView):
	template_name = "settings/user_about_form.html"
	form=None
	profile=None

	def get(self,request,*args,**kwargs):
		self.user=request.user
		self.form=AboutUserForm(instance=self.user)
		return super(UserAboutChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserAboutChange,self).get_context_data(**kwargs)
		context["profile"]=self.profile
		context["form"]=self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user=request.user
		try:
			self.profile=UserProfile.objects.get(user=request.user)
		except:
			self.profile = None
		if not self.profile:
			self.user.profile = UserProfile.objects.create(user=request.user)
		self.form=AboutUserForm(request.POST,instance=self.user.profile)
		if self.form.is_valid():
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(UserAboutChange,self).post(request,*args,**kwargs)


class SettingsNotifyView(TemplateView):
    template_name = "settings/notifications_settings.html"
    form=None
    notify_settings=None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.form=SettingsNotifyForm(instance=self.user)
        return super(SettingsNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(SettingsNotifyView,self).get_context_data(**kwargs)
        context["form"]=self.form
        context["notify_settings"]=self.notify_settings
        return context

    def post(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        try:
            self.notify_settings=UserNotificationsSettings.objects.get(user=request.user)
        except:
            self.notify_settings = None
        if not self.notify_settings:
            self.user.notify_settings = UserNotificationsSettings.objects.create(user=request.user)
        self.form=SettingsNotifyForm(request.POST,instance=self.notify_settings)
        if self.form.is_valid():
            self.form.save()
            if request.is_ajax():
                return HttpResponse ('!')
        return super(SettingsNotifyView,self).post(request,*args,**kwargs)


class SettingsPrivateView(TemplateView):
	template_name = "settings/private_settings.html"
	form=None
	private_settings=None

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.form=SettingsPrivateForm(instance=self.user)
		return super(SettingsPrivateView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(SettingsPrivateView,self).get_context_data(**kwargs)
		context["private_settings"]=self.private_settings
		context["form"]=self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_settings=UserPrivateSettings.objects.get(user=request.user)
		except:
			self.private_settings = None
		if not self.private_settings:
			self.user.private_settings = UserPrivateSettings.objects.create(user=request.user)
		self.form=SettingsPrivateForm(request.POST, instance=self.private_settings)
		if self.form.is_valid():
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(SettingsPrivateView,self).post(request,*args,**kwargs)


class UserDesign(TemplateView):
	template_name="settings/user_design.html"
