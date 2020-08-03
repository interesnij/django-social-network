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
		if request.is_ajax() and self.form.is_valid():
			user = self.request.user
			user.first_name = self.form.cleaned_data['first_name']
			user.last_name = self.form.cleaned_data['last_name']
			user.save()
			self.form.save()
			return HttpResponse ('')
		return super(UserInfoChange,self).post(request,*args,**kwargs)


class UserDesign(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="design.html", request=request)
		return super(UserDesign,self).get(request,*args,**kwargs)


class UserNotifyView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="notify.html", request=request)
		try:
			self.notify = UserNotifications.objects.get(user=self.user)
		except:
			self.notify = UserNotifications.objects.create(user=self.user)
		self.form=UserNotifyForm(instance=self.notify)
		return super(UserNotifyView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify"] = self.notify
		context["user"] = self.user
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.notify = UserNotifications.objects.get(user=self.user)
		self.form = UserNotifyForm(request.POST, instance=self.notify)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse ()

class UserNotifyPostView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="notify_post.html", request=request)
		try:
			self.notify_post = UserNotificationsPost.objects.get(user=self.user)
		except:
			self.notify_post = UserNotificationsPost.objects.create(user=self.user)
		self.form=UserNotifyPostForm(instance=self.notify_post)
		return super(UserNotifyPostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyPostView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_post"] = self.notify_post
		context["user"] = self.user
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.notify_post = UserNotificationsPost.objects.get(user=self.user)
		self.form = UserNotifyPostForm(request.POST, instance=self.notify_post)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse ()

class UserNotifyPhotoView(TemplateView):
	template_name = None
	form = None
	notify_photo = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="notify_photo.html", request=request)
		try:
			self.notify_photo = UserNotificationsPhoto.objects.get(user=self.user)
		except:
			self.notify_photo = UserNotificationsPhoto.objects.create(user=self.user)
		self.form=UserNotifyPhotoForm(instance=self.notify_photo)
		return super(UserNotifyPhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyPhotoView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_photo"] = self.notify_photo
		context["user"] = self.user
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.notify_photo = UserNotificationsPhoto.objects.get(user=self.user)
		self.form = UserNotifyPhotoForm(request.POST, instance=self.notify_photo)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse ()

class UserNotifyGoodView(TemplateView):
	template_name = None
	form = None
	notify_good = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="notify_good.html", request=request)
		try:
			self.notify_good = UserNotificationsGood.objects.get(user=self.user)
		except:
			self.notify_good = UserNotificationsGood.objects.create(user=self.user)
		self.form=UserNotifyGoodForm(instance=self.notify_good)
		return super(UserNotifyGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyGoodView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_good"] = self.notify_good
		context["user"] = self.user
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.notify_good = UserNotificationsGood.objects.get(user=self.user)
		self.form = UserNotifyGoodForm(request.POST, instance=self.notify_good)
		if request.is_ajax() and self.form.is_valid() and request.user == request.user:
			self.form.save()
			return HttpResponse ()

class UserNotifyVideoView(TemplateView):
	template_name = None
	form = None
	notify_video = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="notify_video.html", request=request)
		try:
			self.notify_video = UserNotificationsVideo.objects.get(user=self.user)
		except:
			self.notify_video = UserNotificationsVideo.objects.create(user=self.user)
		self.form = UserNotifyVideoForm(instance=self.notify_video, initial={"user":self.user},)
		return super(UserNotifyVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyVideoView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_video"] = self.notify_video
		context["user"] = self.user
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.notify_video = UserNotificationsVideo.objects.get(user=self.user)
		self.form = UserNotifyVideoForm(request.POST, instance=self.notify_video)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse ()

class UserNotifyMusicView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="settings/", template="notify_music.html", request=request)
		try:
			self.notify_music = UserNotificationsMusic.objects.get(user=self.user)
		except:
			self.notify_music = UserNotificationsMusic.objects.create(user=self.user)
		self.form = UserNotifyMusicForm(instance=self.notify_music, initial={"user":self.user},)
		return super(UserNotifyMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyMusicView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["user"] = self.user
		context["notify_music"] = self.notify_music
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.notify_music = UserNotificationsMusic.objects.get(user=self.user)
		self.form = UserNotifyMusicForm(request.POST, instance=self.notify_music)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse ()
		return super(UserNotifyMusicView,self).post(request,*args,**kwargs)

class UserPrivateView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.private = UserPrivate.objects.get(user=self.user)
		except:
			self.private = UserPrivate.objects.create(user=self.user)
		self.form = UserPrivateForm(instance=self.private)
		self.template_name = self.user.get_settings_template(folder="settings/", template="private.html", request=request)
		return super(UserPrivateView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivateView,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.private = UserPrivate.objects.get(user=self.user)
		self.form = UserPrivateForm(request.POST, instance=self.private)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse()

class UserPrivatePostView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_post = UserPrivatePost.objects.get(user=self.user)
		except:
			self.private_post = UserPrivatePost.objects.create(user=self.user)
		self.form = UserPrivatePostForm(instance=self.private_post)
		self.template_name = self.user.get_settings_template(folder="settings/", template="private_post.html", request=request)
		return super(UserPrivatePostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivatePostView,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.private_post = UserPrivatePost.objects.get(user=self.user)
		self.form = UserPrivatePostForm(request.POST, instance=self.private_post)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse()

class UserPrivateGoodView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_good = UserPrivateGood.objects.get(user=self.user)
		except:
			self.private_good = UserPrivateGood.objects.create(user=self.user)
		self.form = UserPrivateGoodForm(instance=self.private_good)
		self.template_name = self.user.get_settings_template(folder="settings/", template="private_good.html", request=request)
		return super(UserPrivateGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivateGoodView,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.private_good = UserPrivateGood.objects.get(user=self.user)
		self.form = UserPrivateGoodForm(request.POST, instance=self.private_good)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse()

class UserPrivateVideoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_video = UserPrivateVideo.objects.get(user=self.user)
		except:
			self.private_video = UserPrivateVideo.objects.create(user=self.user)
		self.form = UserPrivateVideoForm(instance=self.private_video)
		self.template_name = self.user.get_settings_template(folder="settings/", template="private_video.html", request=request)
		return super(UserPrivateVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivateVideoView,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.private_video = UserPrivateVideo.objects.get(user=self.user)
		self.form = UserPrivateVideoForm(request.POST, instance=self.private_video)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse()

class UserPrivatePhotoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_photo = UserPrivatePhoto.objects.get(user=self.user)
		except:
			self.private_photo = UserPrivatePhoto.objects.create(user=self.user)
		self.form = UserPrivatePhotoForm(instance=self.private_photo)
		self.template_name = self.user.get_settings_template(folder="settings/", template="private_photo.html", request=request)
		return super(UserPrivatePhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivatePhotoView,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.private_photo = UserPrivatePhoto.objects.get(user=self.user)
		self.form = UserPrivatePhotoForm(request.POST, instance=self.private_photo)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse()

class UserPrivateMusicView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_music = UserPrivateMusic.objects.get(user=self.user)
		except:
			self.private_music = UserPrivateMusic.objects.create(user=self.user)
		self.form = UserPrivateMusicForm(instance=self.private_music)
		self.template_name = self.user.get_settings_template(folder="settings/", template="private_music.html", request=request)
		return super(UserPrivateMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivateMusicView,self).get_context_data(**kwargs)
		context["user"] = self.user
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.private_music = UserPrivateMusic.objects.get(user=self.user)
		self.form = UserPrivateMusicForm(request.POST, instance=self.private_music)
		if request.is_ajax() and self.form.is_valid() and self.user == request.user:
			self.form.save()
			return HttpResponse()
