from django.views.generic import ListView
from communities.models import *
from communities.model.settings import *
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from communities.forms import *
from users.models import User
from follows.models import CommunityFollow
from datetime import datetime, timedelta
from common.template.community import get_community_manage_template, get_community_moders_template


class CommunityGeneralView(TemplateView):
	template_name = None
	form=None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=GeneralCommunityForm(instance=self.community)
		self.template_name = get_community_manage_template("communities/manage/general.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityGeneralView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityGeneralView,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["community"]=self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.form=GeneralCommunityForm(request.POST, instance=self.community)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse('!')
		else:
			return HttpResponseBadRequest()
		return super(CommunityGeneralView,self).post(request,*args,**kwargs)


class CommunitySectionsOpenView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/sections.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.sections = CommunitySectionsOpen.objects.get(community=self.community)
		except:
			self.sections = CommunitySectionsOpen.objects.create(community=self.community)
		self.form=CommunitySectionOpenForm(instance=self.sections)
		return super(CommunitySectionsOpenView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunitySectionsOpenView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["sections"] = self.sections
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.sections = CommunitySectionsOpen.objects.get(community=self.community)
		self.form = CommunitySectionOpenForm(request.POST, instance=self.sections)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ()
		return super(CommunitySectionsOpenView,self).post(request,*args,**kwargs)


class CommunityNotifyPostView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_post.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_post = CommunityNotificationsPost.objects.get(community=self.community)
		except:
			self.notify_post = CommunityNotificationsPost.objects.create(community=self.community)
		self.form=CommunityNotifyPostForm(instance=self.notify_post)
		return super(CommunityNotifyPostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyPostView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_post"] = self.notify_post
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_post = CommunityNotificationsPost.objects.get(community=self.community)
		self.form = CommunityNotifyPostForm(request.POST, instance=self.notify_post)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyPostView,self).post(request,*args,**kwargs)

class CommunityNotifyPhotoView(TemplateView):
	template_name = None
	form = None
	notify_photo = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_photo.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_photo = CommunityNotificationsPhoto.objects.get(community=self.community)
		except:
			self.notify_photo = CommunityNotificationsPhoto.objects.create(community=self.community)
		self.form=CommunityNotifyPhotoForm(instance=self.notify_photo)
		return super(CommunityNotifyPhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyPhotoView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_photo"] = self.notify_photo
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_photo = CommunityNotificationsPhoto.objects.get(community=self.community)
		self.form = CommunityNotifyPhotoForm(request.POST, instance=self.notify_photo)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyPhotoView,self).post(request,*args,**kwargs)

class CommunityNotifyGoodView(TemplateView):
	template_name = None
	form = None
	notify_good = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_good.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_good = CommunityNotificationsGood.objects.get(community=self.community)
		except:
			self.notify_good = CommunityNotificationsGood.objects.create(community=self.community)
		self.form=CommunityNotifyGoodForm(instance=self.notify_good)
		return super(CommunityNotifyGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyGoodView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_good"] = self.notify_good
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_good = CommunityNotificationsGood.objects.get(community=self.community)
		self.form = CommunityNotifyGoodForm(request.POST, instance=self.notify_good)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyGoodView,self).post(request,*args,**kwargs)

class CommunityNotifyVideoView(TemplateView):
	template_name = None
	form = None
	notify_video = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_video.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_video = CommunityNotificationsVideo.objects.get(community=self.community)
		except:
			self.notify_video = CommunityNotificationsVideo.objects.create(community=self.community)
		self.form = CommunityNotifyVideoForm(instance=self.notify_video, initial={"community":self.community},)
		return super(CommunityNotifyVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyVideoView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["notify_video"] = self.notify_video
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_video = CommunityNotificationsVideo.objects.get(community=self.community)
		self.form = CommunityNotifyVideoForm(request.POST, instance=self.notify_video)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyVideoView,self).post(request,*args,**kwargs)

class CommunityNotifyMusicView(TemplateView):
	template_name = None
	form = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/notify_music.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_music = CommunityNotificationsMusic.objects.get(community=self.community)
		except:
			self.notify_music = CommunityNotificationsMusic.objects.create(community=self.community)
		self.form = CommunityNotifyMusicForm(instance=self.notify_music, initial={"community":self.community},)
		return super(CommunityNotifyMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyMusicView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["community"] = self.community
		context["notify_music"] = self.notify_music
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.notify_music = CommunityNotificationsMusic.objects.get(community=self.community)
		self.form = CommunityNotifyMusicForm(request.POST, instance=self.notify_music)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyMusicView,self).post(request,*args,**kwargs)

class CommunityPrivatePostView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_post = CommunityPrivatePost.objects.get(community=self.community)
		except:
			self.private_post = CommunityPrivatePost.objects.create(community=self.community)
		self.form = CommunityPrivatePostForm(instance=self.private_post)
		self.template_name = get_community_manage_template("communities/manage/private_post.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityPrivatePostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivatePostView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.private_post = CommunityPrivatePost.objects.get(community=self.community)
		self.form = CommunityPrivatePostForm(request.POST, instance=self.private_post)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateGoodView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_good = CommunityPrivateGood.objects.get(community=self.community)
		except:
			self.private_good = CommunityPrivateGood.objects.create(community=self.community)
		self.form = CommunityPrivateGoodForm(instance=self.private_good)
		self.template_name = get_community_manage_template("communities/manage/private_good.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityPrivateGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivateGoodView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.private_good = CommunityPrivateGood.objects.get(community=self.community)
		self.form = CommunityPrivateGoodForm(request.POST, instance=self.private_good)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateVideoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_video = CommunityPrivateVideo.objects.get(community=self.community)
		except:
			self.private_video = CommunityPrivateVideo.objects.create(community=self.community)
		self.form = CommunityPrivateVideoForm(instance=self.private_video)
		self.template_name = get_community_manage_template("communities/manage/private_video.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityPrivateVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivateVideoView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.private_video = CommunityPrivateVideo.objects.get(community=self.community)
		self.form = CommunityPrivateVideoForm(request.POST, instance=self.private_video)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivatePhotoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_photo = CommunityPrivatePhoto.objects.get(community=self.community)
		except:
			self.private_photo = CommunityPrivatePhoto.objects.create(community=self.community)
		self.form = CommunityPrivatePhotoForm(instance=self.private_photo)
		self.template_name = get_community_manage_template("communities/manage/private_photo.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityPrivatePhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivatePhotoView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.private_photo = CommunityPrivatePhoto.objects.get(community=self.community)
		self.form = CommunityPrivatePhotoForm(request.POST, instance=self.private_photo)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateMusicView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.private_music = CommunityPrivateMusic.objects.get(community=self.community)
		except:
			self.private_music = CommunityPrivateMusic.objects.create(community=self.community)
		self.form = CommunityPrivateMusicForm(instance=self.private_music)
		self.template_name = get_community_manage_template("communities/manage/private_music.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityPrivateMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivateMusicView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = self.form
		return context

	def post(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.private_music = CommunityPrivateMusic.objects.get(community=self.community)
		self.form = CommunityPrivateMusicForm(request.POST, instance=self.private_music)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityAdminView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/admins.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityAdminView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityAdminView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		admins = self.community.get_community_administrators(self.community.pk)
		return admins


class CommunityEditorsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/editors.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityEditorsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityEditorsView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		admins = self.community.get_community_editors(self.community.pk)
		return admins


class CommunityAdvertisersView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/advertisers.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityAdvertisersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityAdvertisersView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		advertisers = self.community.get_community_advertisers(self.community.pk)
		return advertisers


class CommunityModersView(ListView):
	template_name="manage/moders.html"
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/moders.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityModersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityModersView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		moders=self.community.get_community_moderators(self.community.pk)
		return moders


class CommunityBlackListView(ListView):
	template_name="manage/black_list.html"
	model=User
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_moders_template("communities/manage/moders.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityBlackListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityBlackListView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		black_list=self.community.get_community_banned_users(self.community.pk)
		return black_list


class CommunityFollowsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/manage/follows.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityFollowsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityFollowsView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		follows = CommunityFollow.get_community_follows(self.community.pk)
		return follows


class CommunityMemberManageView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.administrators = Community.get_community_administrators(self.community.pk)
		self.moderators = Community.get_community_moderators(self.community.pk)
		self.editors = Community.get_community_editors(self.community.pk)
		self.advertisers = Community.get_community_advertisers(self.community.pk)
		self.template_name = get_community_manage_template("communities/manage/members.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityMemberManageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityMemberManageView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["administrators"] = self.administrators
		context["moderators"] = self.moderators
		context["editors"] = self.editors
		context["advertisers"] = self.advertisers
		return context

	def get_queryset(self):
		membersheeps = self.community.get_community_members(self.community.pk)
		return membersheeps


class CommunityStaffWindow(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		self.administrator = self.user.is_administrator_of_community(self.community.pk)
		self.moderator = self.user.is_moderator_of_community(self.community.pk)
		self.editor = self.user.is_editor_of_community(self.community.pk)
		self.advertiser = self.user.is_advertiser_of_community(self.community.pk)
		self.template_name = get_community_manage_template("communities/manage/staff_window.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityStaffWindow,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityStaffWindow,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["user"] = self.user
		context["administrator"] = self.administrator
		context["moderator"] = self.moderator
		context["editor"] = self.editor
		context["advertiser"] = self.advertiser
		return context
