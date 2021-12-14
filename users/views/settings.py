from django.views.generic.base import TemplateView
from users.model.profile import UserProfile
from users.model.settings import *
from users.forms import *
from django.http import HttpResponse, HttpResponseBadRequest
from users.models import User
from common.templates import get_settings_template


class UserGeneralChange(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/general.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserGeneralChange,self).get(request,*args,**kwargs)


class UserInfoChange(TemplateView):
	template_name, form, profile = None, None, None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/info.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserInfoChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserInfoChange,self).get_context_data(**kwargs)
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.form = InfoUserForm(request.POST,instance=request.user)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse ('')
		return super(UserInfoChange,self).post(request,*args,**kwargs)


class UserDesign(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		try:
			self.color = UserColorSettings.objects.get(user=request.user)
		except:
			self.color = UserColorSettings.objects.create(user=request.user)
		self.template_name = get_settings_template("users/settings/design.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserDesign,self).get(request,*args,**kwargs)


class UserNotifyView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/notify.html", request.user, request.META['HTTP_USER_AGENT'])
		try:
			self.notify = UserNotifications.objects.get(user=request.user)
		except:
			self.notify = UserNotifications.objects.create(user=request.user)
		self.form=UserNotifyForm(instance=self.notify)
		return super(UserNotifyView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify"] = self.notify
		context["user"] = self.request.user
		return context

	def post(self,request,*args,**kwargs):
		self.notify = UserNotifications.objects.get(user=request.user)
		self.form = UserNotifyForm(request.POST, instance=self.notify)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse ()

class UserNotifyPostView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/notify_post.html", request.user, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_post = UserNotificationsPost.objects.get(user=request.user)
		except:
			self.notify_post = UserNotificationsPost.objects.create(user=request.user)
		self.form=UserNotifyPostForm(instance=self.notify_post)
		return super(UserNotifyPostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyPostView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_post"] = self.notify_post
		context["user"] = self.request.user
		return context

	def post(self,request,*args,**kwargs):
		self.notify_post = UserNotificationsPost.objects.get(user=request.user)
		self.form = UserNotifyPostForm(request.POST, instance=self.notify_post)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse ()

class UserNotifyPhotoView(TemplateView):
	template_name = None
	form = None
	notify_photo = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/notify_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_photo = UserNotificationsPhoto.objects.get(user=request.user)
		except:
			self.notify_photo = UserNotificationsPhoto.objects.create(user=request.user)
		self.form=UserNotifyPhotoForm(instance=self.notify_photo)
		return super(UserNotifyPhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyPhotoView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_photo"] = self.notify_photo
		context["user"] = self.request.user
		return context

	def post(self,request,*args,**kwargs):
		self.notify_photo = UserNotificationsPhoto.objects.get(user=request.user)
		self.form = UserNotifyPhotoForm(request.POST, instance=self.notify_photo)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse ()

class UserNotifyGoodView(TemplateView):
	template_name = None
	form = None
	notify_good = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/notify_good.html", request.user, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_good = UserNotificationsGood.objects.get(user=request.user)
		except:
			self.notify_good = UserNotificationsGood.objects.create(user=request.user)
		self.form=UserNotifyGoodForm(instance=self.notify_good)
		return super(UserNotifyGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyGoodView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_good"] = self.notify_good
		context["user"] = self.request.user
		return context

	def post(self,request,*args,**kwargs):
		self.notify_good = UserNotificationsGood.objects.get(user=request.user)
		self.form = UserNotifyGoodForm(request.POST, instance=self.notify_good)
		if request.is_ajax() and self.form.is_valid() and request.user == request.user:
			self.form.save()
			return HttpResponse ()

class UserNotifyVideoView(TemplateView):
	template_name = None
	form = None
	notify_video = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/notify_video.html", request.user, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_video = UserNotificationsVideo.objects.get(user=request.user)
		except:
			self.notify_video = UserNotificationsVideo.objects.create(user=request.user)
		self.form = UserNotifyVideoForm(instance=self.notify_video, initial={"user":request.user},)
		return super(UserNotifyVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyVideoView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_video"] = self.notify_video
		context["user"] = self.request.user
		return context

	def post(self,request,*args,**kwargs):
		self.notify_video = UserNotificationsVideo.objects.get(user=request.user)
		self.form = UserNotifyVideoForm(request.POST, instance=self.notify_video)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse ()

class UserNotifyMusicView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/notify_music.html", request.user, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_music = UserNotificationsMusic.objects.get(user=request.user)
		except:
			self.notify_music = UserNotificationsMusic.objects.create(user=request.user)
		self.form = UserNotifyMusicForm(instance=self.notify_music, initial={"user":request.user},)
		return super(UserNotifyMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserNotifyMusicView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["user"] = self.request.user
		context["notify_music"] = self.notify_music
		return context

	def post(self,request,*args,**kwargs):
		self.notify_music = UserNotificationsMusic.objects.get(user=request.user)
		self.form = UserNotifyMusicForm(request.POST, instance=self.notify_music)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse ()
		return super(UserNotifyMusicView,self).post(request,*args,**kwargs)

class UserPrivateView(TemplateView):
	template_name = None
	def get(self,request,*args,**kwargs):
		try:
			self.private = ProfilePrivate.objects.get(user=request.user)
		except UserPrivate.DoesNotExist:
			self.private = ProfilePrivate.objects.create(user=request.user)
		self.template_name = get_settings_template("users/settings/perm/private.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPrivateView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivateView,self).get_context_data(**kwargs)
		context["private"] = self.private
		return context

	def post(self,request,*args,**kwargs):
		try:
			private = ProfilePrivate.objects.get(user=request.user)
		except UserPrivate.DoesNotExist:
			private = ProfilePrivate.objects.create(user=request.user)

		type = request.GET.get("action")
		value = request.GET.get("value")
		if not request.is_ajax() or value == 17 or value == 18:
			return HttpResponse(value)
		if type[:3] == "can":
			if type == "can_see_community":
				private.can_see_community = value
				private.save(update_fields=["can_see_community"])
			elif type == "can_see_info":
				private.can_see_info = value
				private.save(update_fields=["can_see_info"])
			elif type == "can_see_friend":
				private.can_see_friend = value
				private.save(update_fields=["can_see_friend"])
			elif type == "can_send_message":
				private.can_send_message = value
				private.save(update_fields=["can_send_message"])
			elif type == "can_add_in_chat":
				private.can_add_in_chat = value
				private.save(update_fields=["can_add_in_chat"])
			elif type == "can_see_post":
				private.can_see_post = value
				private.save(update_fields=["can_see_post"])
			elif type == "can_see_photo":
				private.can_see_photo = value
				private.save(update_fields=["can_see_photo"])
			elif type == "can_see_good":
				private.can_see_good = value
				private.save(update_fields=["can_see_good"])
			elif type == "can_see_video":
				private.can_see_video = value
				private.save(update_fields=["can_see_video"])
			elif type == "can_see_music":
				private.can_see_music = value
				private.save(update_fields=["can_see_music"])
			elif type == "can_see_planner":
				private.can_see_planner = value
				private.save(update_fields=["can_see_planner"])
			elif type == "can_see_doc":
				private.can_see_doc = value
				private.save(update_fields=["can_see_doc"])
		return HttpResponse()


class UserEditName(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/edit_name.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserEditName,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserNameForm
		context = super(UserEditName,self).get_context_data(**kwargs)
		context["form"] = UserNameForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserNameForm

		self.form = UserNameForm(request.POST,instance=request.user)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()
		return super(UserEditName,self).post(request,*args,**kwargs)

class UserEditPassword(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/edit_password.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserEditPassword,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserPasswordForm
		context = super(UserEditPassword,self).get_context_data(**kwargs)
		context["form"] = UserPasswordForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserPasswordForm

		self.form = UserPasswordForm(request.POST,instance=request.user)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()
		return super(UserEditPassword,self).post(request,*args,**kwargs)

class UserEditEmail(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/edit_email.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserEditEmail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserEmailForm
		context = super(UserEditEmail,self).get_context_data(**kwargs)
		context["form"] = UserEmailForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserEmailForm

		self.form = UserEmailForm(request.POST,instance=request.user)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()
		return super(UserEditEmail,self).post(request,*args,**kwargs)

class UserEditPhone(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/edit_phone.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserEditPhone,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from users.forms import UserPhoneForm
		context = super(UserEditPhone,self).get_context_data(**kwargs)
		context["form"] = UserPhoneForm()
		return context

	def post(self,request,*args,**kwargs):
		from users.forms import UserPhoneForm

		self.form = UserPhoneForm(request.POST,instance=request.user)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()
		return super(UserEditPhone,self).post(request,*args,**kwargs)

class UserEditLink(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/edit_link.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserEditLink,self).get(request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		from common.model.other import CustomLink
		if request.is_ajax():
			link = request.POST.get('link')
			if CustomLink.objects.filter(link=link).exists():
				return HttpResponse()
			else:
				CustomLink.objects.create(link=link, user=request.user)
				request.user.have_link = link
				request.user.save(update_fields=['have_link'])
				return HttpResponse()

class UserVerifySend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/verify_send.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVerifySend,self).get(request,*args,**kwargs)

class UserIdentifySend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/identify_send.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserIdentifySend,self).get(request,*args,**kwargs)

class UserRemoveProfile(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/remove_profile.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserRemoveProfile,self).get(request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		from users.forms import UserDeletedForm

		self.form = UserDeletedForm(request.POST)
		if request.is_ajax() or self.form.is_valid():
			request.user.type = User.DELETED
			request.user.save(update_fields=['type'])
			post = self.form.save(commit=False)
			UserDeleted.objects.create(user=request.user.pk, answer=post.answer, other=post.other)
			return HttpResponse()


class UserPrivateExcludeUsers(ListView):
	template_name, users = None, []

	def get(self,request,*args,**kwargs):
		self.type = request.GET.get("action")
		if self.type == "can_see_community":
			self.users = request.user.get_can_see_community_exclude_users()
			self.text = "видеть сообщества"
		if self.chat.is_user_can_edit_info(request.user):
			self.template_name = get_settings_template("users/settings/perm/exclude_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPrivateExcludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivateExcludeUsers,self).get_context_data(**kwargs)
		context["users"] = self.users
		context["text"] = self.text
		context["type"] = self.type
		return context

	def get_queryset(self):
		return self.request.user.get_all_friends()

	def post(self,request,*args,**kwargs):
		from django.http import HttpResponse

		if request.is_ajax():
			request.user.post_exclude_users(request.POST.getlist("users"), request.POST.get("type"))
			return HttpResponse('ok')
		return HttpResponse('not ok')
