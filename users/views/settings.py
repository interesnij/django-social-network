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
		self.template_name = get_settings_template("users/settings/general.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserGeneralChange,self).get(request,*args,**kwargs)


class UserInfoChange(TemplateView):
	template_name, form, profile = None, None, None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/info.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/design.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserDesign,self).get(request,*args,**kwargs)


class UserNotifyView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/notify.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/notify_post.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/notify_photo.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/notify_good.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/notify_video.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/notify_music.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.private = UserPrivate.objects.get(user=request.user)
		self.form = UserPrivateForm(instance=self.private)
		self.template_name = get_settings_template("users/settings/private.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserPrivateView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPrivateView,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.private = UserPrivate.objects.get(user=request.user)
		self.form = UserPrivateForm(request.POST, instance=self.private)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()

class UserPrivatePostView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.list = request.user.get_post_list()
		self.template_name = get_settings_template("users/settings/private_post.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserPrivatePostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from posts.forms import PostsListForm

		context = super(UserPrivatePostView,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = PostsListForm(instance=self.list)
		context["list"] = self.list
		return context

	def post(self,request,*args,**kwargs):
		from posts.forms import PostsListForm

		self.list = request.user.get_post_list()
		self.form = PostsListForm(instance=self.list)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()

class UserPrivateGoodView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.list = request.user.get_good_list()
		self.template_name = get_settings_template("users/settings/private_good.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserPrivateGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from goods.forms import GoodListForm

		context = super(UserPrivateGoodView,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = GoodListForm(instance=self.list)
		context["list"] = self.list
		return context

	def post(self,request,*args,**kwargs):
		from goods.forms import GoodListForm

		self.list = request.user.get_good_list()
		self.form = GoodListForm(instance=self.list)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()

class UserPrivateVideoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.list = request.user.get_video_list()
		self.template_name = get_settings_template("users/settings/private_video.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserPrivateVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from video.forms import VideoListForm

		context = super(UserPrivateVideoView,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = VideoListForm(instance=self.list)
		context["list"] = self.list
		return context

	def post(self,request,*args,**kwargs):
		from video.forms import VideoListForm

		self.list = request.user.get_video_list()
		self.form = VideoListForm(instance=self.list)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()

class UserPrivatePhotoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.list = request.user.get_photo_list()
		self.template_name = get_settings_template("users/settings/private_photo.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserPrivatePhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from gallery.forms import PhotoListForm

		context = super(UserPrivatePhotoView,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = PhotoListForm(instance=self.list)
		context["list"] = self.list
		return context

	def post(self,request,*args,**kwargs):
		from gallery.forms import PhotoListForm

		self.list = request.user.get_photo_list()
		self.form = PhotoListForm(instance=self.list)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()

class UserPrivateMusicView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.list = request.user.get_playlist()
		self.template_name = get_settings_template("users/settings/private_music.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserPrivateMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from music.forms import PlaylistForm

		context = super(UserPrivateMusicView,self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["form"] = PlaylistForm(instance=self.list)
		context["list"] = self.list
		return context

	def post(self,request,*args,**kwargs):
		from music.forms import PlaylistForm

		self.list = request.user.get_playlist()
		self.form = PlaylistForm(instance=self.list)
		if request.is_ajax() and self.form.is_valid():
			self.form.save()
			return HttpResponse()


class UserEditName(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/edit_name.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/edit_password.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/edit_email.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/edit_phone.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/edit_link.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
		self.template_name = get_settings_template("users/settings/verify_send.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserVerifySend,self).get(request,*args,**kwargs)

class UserIdentifySend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/identify_send.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
		return super(UserIdentifySend,self).get(request,*args,**kwargs)

class UserRemoveProfile(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/settings/remove_profile.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
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
