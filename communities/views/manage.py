from django.views.generic import ListView
from communities.models import Community
from communities.model.settings import *
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from communities.forms import *
from common.templates import get_community_manage_template, get_community_moders_template


class CommunityGeneralView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.form, self.template_name = GeneralCommunityForm(instance=self.c), get_community_manage_template("communities/manage/general.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		return super(CommunityGeneralView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityGeneralView,self).get_context_data(**kwargs)
		c["form"], c["community"] = self.form, self.c
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.form = GeneralCommunityForm(request.POST, instance=self.c)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse()
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()
		return super(CommunityGeneralView,self).post(request,*args,**kwargs)


class CommunitySectionsOpenView(TemplateView):
	template_name = None

	def get(self, request, *args, **kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/sections.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.private = CommunityPrivate2.objects.get(community=self.c)
		except:
			self.private = CommunityPrivate2.objects.create(community=self.c)
		return super(CommunitySectionsOpenView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunitySectionsOpenView,self).get_context_data(**kwargs)
		c["private"], c["community"] = self.private, self.c
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.private = CommunityPrivate2.objects.get(community=self.c)
		if not self.c.is_user_can_see_settings(request.user.pk):
			return HttpResponse("Кыш отсюда!")
		type = request.GET.get("action")
		value = request.GET.get("value")
		if not request.is_ajax() or value == 5 or value == 6:
			return HttpResponse(value)
		if type[:3] == "can":
			if type == "can_see_info":
				private.can_see_info = value
				private.save(update_fields=["can_see_info"])
			elif type == "can_see_member":
				private.can_see_member = value
				private.save(update_fields=["can_see_member"])
			elif type == "can_send_message":
				private.can_send_message = value
				private.save(update_fields=["can_send_message"])
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
			elif type == "can_see_settings":
				private.can_see_settings = value
				private.save(update_fields=["can_see_settings"])
			elif type == "can_see_log":
				private.can_see_log = value
				private.save(update_fields=["can_see_log"])
			elif type == "can_see_stat":
				private.can_see_stat = value
				private.save(update_fields=["can_see_stat"])
		return super(CommunitySectionsOpenView,self).post(request,*args,**kwargs)


class CommunityNotifyPostView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_post.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_post = CommunityNotificationsPost.objects.get(community=self.c)
		except:
			self.notify_post = CommunityNotificationsPost.objects.create(community=self.c)
		return super(CommunityNotifyPostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityNotifyPostView,self).get_context_data(**kwargs)
		c["form"], c["notify_post"], c["community"] = CommunityNotifyPostForm(instance=self.notify_post), self.notify_post, self.c
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_post, self.form = CommunityNotificationsPost.objects.get(community=self.c), CommunityNotifyPostForm(request.POST, instance=self.notify_post)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyPostView,self).post(request,*args,**kwargs)

class CommunityNotifyPhotoView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_photo.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_photo = CommunityNotificationsPhoto.objects.get(community=self.c)
		except:
			self.notify_photo = CommunityNotificationsPhoto.objects.create(community=self.c)
		return super(CommunityNotifyPhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityNotifyPhotoView,self).get_context_data(**kwargs)
		c["form"], c["notify_photo"], c["community"] = CommunityNotifyPhotoForm(instance=self.notify_photo), self.notify_photo, self.notify_photo
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_photo, self.form = CommunityNotificationsPhoto.objects.get(community=self.c), CommunityNotifyPhotoForm(request.POST, instance=self.notify_photo)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyPhotoView,self).post(request,*args,**kwargs)

class CommunityNotifyGoodView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_good.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_good = CommunityNotificationsGood.objects.get(community=self.c)
		except:
			self.notify_good = CommunityNotificationsGood.objects.create(community=self.c)
		return super(CommunityNotifyGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityNotifyGoodView,self).get_context_data(**kwargs)
		c["form"], c["notify_good"], c["community"] = CommunityNotifyGoodForm(instance=self.notify_good), self.notify_good, self.c
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_good, self.form = CommunityNotificationsGood.objects.get(community=self.c), CommunityNotifyGoodForm(request.POST, instance=self.notify_good)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyGoodView,self).post(request,*args,**kwargs)

class CommunityNotifyVideoView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_video.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_video = CommunityNotificationsVideo.objects.get(community=self.c)
		except:
			self.notify_video = CommunityNotificationsVideo.objects.create(community=self.c)
		return super(CommunityNotifyVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityNotifyVideoView,self).get_context_data(**kwargs)
		c["form"], c["notify_video"], c["community"] = CommunityNotifyVideoForm(instance=self.notify_video), self.notify_video, self.c
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_video, self.form = CommunityNotificationsVideo.objects.get(community=self.c), CommunityNotifyVideoForm(request.POST, instance=self.notify_video)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyVideoView,self).post(request,*args,**kwargs)

class CommunityNotifyMusicView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_music.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_music = CommunityNotificationsMusic.objects.get(community=self.c)
		except:
			self.notify_music = CommunityNotificationsMusic.objects.create(community=self.c)
		return super(CommunityNotifyMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityNotifyMusicView,self).get_context_data(**kwargs)
		c["community"], c["form"], c["notify_music"] = self.c, CommunityNotifyMusicForm(instance=self.notify_music), self.notify_music
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_music, self.form = CommunityNotificationsMusic.objects.get(community=self.c), CommunityNotifyMusicForm(request.POST, instance=self.notify_music)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyMusicView,self).post(request,*args,**kwargs)

class CommunityAdminView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/admins.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		return super(CommunityAdminView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityAdminView,self).get_context_data(**kwargs)
		context["community"] = self.c
		return context

	def get_queryset(self):
		return self.c.get_administrators(self.c.pk)


class CommunityEditorsView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/editors.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		return super(CommunityEditorsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityEditorsView,self).get_context_data(**kwargs)
		context["community"] = self.c
		return context

	def get_queryset(self):
		return self.c.get_editors(self.c.pk)


class CommunityAdvertisersView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/advertisers.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		return super(CommunityAdvertisersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityAdvertisersView,self).get_context_data(**kwargs)
		context["community"] = self.c
		return context

	def get_queryset(self):
		return self.c.get_advertisers(self.c.pk)


class CommunityModersView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/moders.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		return super(CommunityModersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityModersView,self).get_context_data(**kwargs)
		context["community"]=self.c
		return context

	def get_queryset(self):
		return self.c.get_moderators(self.c.pk)


class CommunityBlackListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_moders_template("communities/manage/moders.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		return super(CommunityBlackListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityBlackListView,self).get_context_data(**kwargs)
		context["community"]=self.c
		return context

	def get_queryset(self):
		return self.c.get_community_banned_users(self.c.pk)


class CommunityFollowsView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/follows.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		return super(CommunityFollowsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityFollowsView,self).get_context_data(**kwargs)
		context["community"] = self.c
		return context

	def get_queryset(self):
		from follows.models import CommunityFollow

		return CommunityFollow.get_community_follows(self.c.pk)


class CommunityMemberManageView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.a, self.m, self.e, self.ad, self.template_name = Community.get_administrators(self.c.pk),Community.get_moderators(self.c.pk),Community.get_editors(self.c.pk),Community.get_advertisers(self.c.pk),get_community_manage_template("communities/manage/members.html", request.user, self.c.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityMemberManageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityMemberManageView,self).get_context_data(**kwargs)
		c["community"], c["administrators"], c["moderators"], c["editors"], c["advertisers"] = self.c, self.m, self.e, self.ad,
		return c

	def get_queryset(self):
		return self.c.get_members(self.c.pk)


class CommunityStaffWindow(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from users.models import User

		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.user, self.administrator, self.moderator, self.editor, self.advertiser, self.template_name = User.objects.get(uuid=self.kwargs["uuid"]), self.user.is_administrator_of_community(self.c.pk), self.user.is_moderator_of_community(self.c.pk), \
		self.user.is_editor_of_community(self.c.pk), self.user.is_advertiser_of_community(self.c.pk), get_community_manage_template("communities/manage/staff_window.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		return super(CommunityStaffWindow,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityStaffWindow,self).get_context_data(**kwargs)
		c["community"], c["user"], c["administrator"], c["moderator"], c["editor"], c["advertiser"] = self.c, self.user, self.administrator, self.moderator, self.editor, self.advertiser
		return c


class CommunityPrivateExcludeUsers(ListView):
	template_name, users = None, []

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.type = request.GET.get("action")
		if self.type == "can_see_info":
			self.users = self.community.get_can_see_info_exclude_users()
			self.text = "видеть информацию сообщества"
		elif self.type == "can_see_member":
			self.users = self.community.get_can_see_member_exclude_users()
			self.text = "видеть подписчиков"
		elif self.type == "can_send_message":
			self.users = self.community.get_can_send_message_exclude_users()
			self.text = "писать сообщения"
		elif self.type == "can_see_post":
			self.users = self.community.get_can_see_post_exclude_users()
			self.text = "видеть записи"
		elif self.type == "can_see_photo":
			self.users = self.community.get_can_see_photo_exclude_users()
			self.text = "видеть фотографии"
		elif self.type == "can_see_good":
			self.users = self.community.get_can_see_good_exclude_users()
			self.text = "видеть товары"
		elif self.type == "can_see_video":
			self.users = self.community.get_can_see_video_exclude_users()
			self.text = "видеть видеозаписи"
		elif self.type == "can_see_music":
			self.users = self.community.get_can_see_music_exclude_users()
			self.text = "видеть аудиозаписи"
		elif self.type == "can_see_planner":
			self.users = self.community.get_can_see_planner_exclude_users()
			self.text = "видеть раздел планирования"
		elif self.type == "can_see_doc":
			self.users = self.community.get_can_see_doc_exclude_users()
			self.text = "видеть документы"
		elif self.type == "can_see_settings":
			self.users = self.community.get_can_see_settings_exclude_users()
			self.text = "видеть настройки"
		elif self.type == "can_see_log":
			self.users = self.community.get_can_see_log_exclude_users()
			self.text = "видеть жернал действий"
		elif self.type == "can_see_stat":
			self.users = self.community.get_can_see_stat_exclude_users()
			self.text = "видеть статистику"
		self.template_name = get_community_manage_template("communities/manage/perm/exclude_users.html", request.user, self.community, request.META['HTTP_USER_AGENT'])
		return super(CommunityPrivateExcludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivateExcludeUsers,self).get_context_data(**kwargs)
		context["users"] = self.users
		context["text"] = self.text
		context["type"] = self.type
		return context

	def get_queryset(self):
		return self.community.get_members()

	def post(self,request,*args,**kwargs):
		from django.http import HttpResponse

		if request.is_ajax():
			self.community.post_exclude_users(request.POST.getlist("users"), request.POST.get("type"))
			return HttpResponse('ok')
		return HttpResponse('not ok')

class CommunityPrivateIncludeUsers(ListView):
	template_name, users = None, []

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.type = request.GET.get("action")
		if self.type == "can_see_info":
			self.users = self.community.get_can_see_info_include_users()
			self.text = "видеть информацию профиля"
		elif self.type == "can_see_member":
			self.users = self.community.get_can_see_member_include_users()
			self.text = "видеть подписчиков"
		elif self.type == "can_send_message":
			self.users = self.community.get_can_send_message_include_users()
			self.text = "писать сообщения"
		elif self.type == "can_see_post":
			self.users = self.community.get_can_see_post_include_users()
			self.text = "видеть записи"
		elif self.type == "can_see_photo":
			self.users = self.community.get_can_see_photo_include_users()
			self.text = "видеть фотографии"
		elif self.type == "can_see_good":
			self.users = self.community.get_can_see_good_include_users()
			self.text = "видеть товары"
		elif self.type == "can_see_video":
			self.users = self.community.get_can_see_video_include_users()
			self.text = "видеть видеозаписи"
		elif self.type == "can_see_music":
			self.users = self.community.get_can_see_music_include_users()
			self.text = "видеть аудиозаписи"
		elif self.type == "can_see_planner":
			self.users = self.community.get_can_see_planner_include_users()
			self.text = "видеть раздел планирования"
		elif self.type == "can_see_doc":
			self.users = self.community.get_can_see_doc_include_users()
			self.text = "видеть документы"
		elif self.type == "can_see_settings":
			self.users = self.community.get_can_see_settings_include_users()
			self.text = "видеть настройки"
		elif self.type == "can_see_log":
			self.users = self.community.get_can_see_log_include_users()
			self.text = "видеть жернал действий"
		elif self.type == "can_see_stat":
			self.users = self.community.get_can_see_stat_include_users()
			self.text = "видеть статистику"
		self.template_name = get_community_manage_template("communities/manage/perm/include_users.html", request.user, self.community, request.META['HTTP_USER_AGENT'])
		return super(CommunityPrivateIncludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivateIncludeUsers,self).get_context_data(**kwargs)
		context["users"] = self.users
		context["text"] = self.text
		context["type"] = self.type
		return context

	def get_queryset(self):
		return self.community.get_members()

	def post(self,request,*args,**kwargs):
		from django.http import HttpResponse

		if request.is_ajax():
			self.community.post_include_users(request.POST.getlist("users"), request.POST.get("type"))
			return HttpResponse('ok')
		return HttpResponse('not ok')
