from django.views.generic import ListView
from communities.models import Community
from communities.model.settings import *
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from communities.forms import *
from common.template.community import get_community_manage_template


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
	template_name, form = None, None

	def get(self, request, *args, **kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/sections.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.sections = CommunitySectionsOpen.objects.get(community=self.c)
		except:
			self.sections = CommunitySectionsOpen.objects.create(community=self.c)
		return super(CommunitySectionsOpenView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunitySectionsOpenView,self).get_context_data(**kwargs)
		c["form"], c["sections"], c["community"] = CommunitySectionOpenForm(instance=self.sections), self.sections, self.c
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.sections, self.form = CommunitySectionsOpen.objects.get(community=self.c), CommunitySectionOpenForm(request.POST, instance=self.sections)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse ()
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

class CommunityPrivatePostView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/private_post.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.private_post = CommunityPrivatePost.objects.get(community=self.c)
		except:
			self.private_post = CommunityPrivatePost.objects.create(community=self.c)
		return super(CommunityPrivatePostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityPrivatePostView,self).get_context_data(**kwargs)
		c["community"], c["form"] = self.c, CommunityPrivatePostForm(instance=self.private_post)
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.private_post, self.form = CommunityPrivatePost.objects.get(community=self.c), CommunityPrivatePostForm(request.POST, instance=self.private_post)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateGoodView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/private_good.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.private_good = CommunityPrivateGood.objects.get(community=self.c)
		except:
			self.private_good = CommunityPrivateGood.objects.create(community=self.c)
		return super(CommunityPrivateGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityPrivateGoodView,self).get_context_data(**kwargs)
		c["community"], c["form"] = self.c, CommunityPrivateGoodForm(instance=self.private_good)
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.private_good, self.form = CommunityPrivateGood.objects.get(community=self.c), CommunityPrivateGoodForm(request.POST, instance=self.private_good)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateVideoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/private_video.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.private_video = CommunityPrivateVideo.objects.get(community=self.c)
		except:
			self.private_video = CommunityPrivateVideo.objects.create(community=self.c)
		return super(CommunityPrivateVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityPrivateVideoView,self).get_context_data(**kwargs)
		c["community"], c["form"] = self.c, CommunityPrivateVideoForm(instance=self.private_video)
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.private_video, self.form = CommunityPrivateVideo.objects.get(community=self.c), CommunityPrivateVideoForm(request.POST, instance=self.private_video)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivatePhotoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/private_photo.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.private_photo = CommunityPrivatePhoto.objects.get(community=self.c)
		except:
			self.private_photo = CommunityPrivatePhoto.objects.create(community=self.c)
		return super(CommunityPrivatePhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityPrivatePhotoView,self).get_context_data(**kwargs)
		c["community"], c["form"] = self.c, CommunityPrivatePhotoForm(instance=self.private_photo)
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.private_photo, self.form = CommunityPrivatePhoto.objects.get(community=self.c), CommunityPrivatePhotoForm(request.POST, instance=self.private_photo)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateMusicView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/private_music.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
		try:
			self.private_music = CommunityPrivateMusic.objects.get(community=self.c)
		except:
			self.private_music = CommunityPrivateMusic.objects.create(community=self.c)
		return super(CommunityPrivateMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityPrivateMusicView,self).get_context_data(**kwargs)
		c["community"], c["form"] = self.c, CommunityPrivateMusicForm(instance=self.private_music)
		return c

	def post(self,request,*args,**kwargs):
		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.private_music, self.form = CommunityPrivateMusic.objects.get(community=self.c), CommunityPrivateMusicForm(request.POST, instance=self.private_music)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
			self.form.save()
			return HttpResponse()

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
		from common.template.community import get_community_moders_template

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
