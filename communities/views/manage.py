from django.views.generic import ListView
from communities.models import Community
from communities.model.settings import *
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest
from communities.forms import *
from common.template.community import get_community_manage_template, get_community_moders_template


class CommunityGeneralView(TemplateView):
	template_name = None
	form=None

	def get(self,request,*args,**kwargs):
		self.community, self.form, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), GeneralCommunityForm(instance=self.community), get_community_manage_template("communities/manage/general.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityGeneralView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityGeneralView,self).get_context_data(**kwargs)
		context["form"] = self.form
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.form = Community.objects.get(pk=self.kwargs["pk"]), GeneralCommunityForm(request.POST, instance=self.community)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse('!')
		else:
			return HttpResponseBadRequest()
		return super(CommunityGeneralView,self).post(request,*args,**kwargs)


class CommunitySectionsOpenView(TemplateView):
	template_name, form = None, None

	def get(self, request, *args, **kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/sections.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.sections = CommunitySectionsOpen.objects.get(community=self.community)
		except:
			self.sections = CommunitySectionsOpen.objects.create(community=self.community)
		return super(CommunitySectionsOpenView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunitySectionsOpenView,self).get_context_data(**kwargs)
		context["form"] = CommunitySectionOpenForm(instance=self.sections)
		context["sections"] = self.sections
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.sections, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunitySectionsOpen.objects.get(community=self.community), CommunitySectionOpenForm(request.POST, instance=self.sections)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ()
		return super(CommunitySectionsOpenView,self).post(request,*args,**kwargs)


class CommunityNotifyPostView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/notify_post.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_post = CommunityNotificationsPost.objects.get(community=self.community)
		except:
			self.notify_post = CommunityNotificationsPost.objects.create(community=self.community)
		return super(CommunityNotifyPostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyPostView,self).get_context_data(**kwargs)
		context["form"] = CommunityNotifyPostForm(instance=self.notify_post)
		context["notify_post"] = self.notify_post
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.notify_post, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityNotificationsPost.objects.get(community=self.community), CommunityNotifyPostForm(request.POST, instance=self.notify_post)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyPostView,self).post(request,*args,**kwargs)

class CommunityNotifyPhotoView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/notify_photo.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_photo = CommunityNotificationsPhoto.objects.get(community=self.community)
		except:
			self.notify_photo = CommunityNotificationsPhoto.objects.create(community=self.community)
		return super(CommunityNotifyPhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyPhotoView,self).get_context_data(**kwargs)
		context["form"] = CommunityNotifyPhotoForm(instance=self.notify_photo)
		context["notify_photo"] = self.notify_photo
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.notify_photo, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityNotificationsPhoto.objects.get(community=self.community), CommunityNotifyPhotoForm(request.POST, instance=self.notify_photo)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyPhotoView,self).post(request,*args,**kwargs)

class CommunityNotifyGoodView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/notify_good.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_good = CommunityNotificationsGood.objects.get(community=self.community)
		except:
			self.notify_good = CommunityNotificationsGood.objects.create(community=self.community)
		return super(CommunityNotifyGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyGoodView,self).get_context_data(**kwargs)
		context["form"] = CommunityNotifyGoodForm(instance=self.notify_good)
		context["notify_good"] = self.notify_good
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.notify_good, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityNotificationsGood.objects.get(community=self.community), CommunityNotifyGoodForm(request.POST, instance=self.notify_good)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyGoodView,self).post(request,*args,**kwargs)

class CommunityNotifyVideoView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/notify_video.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_video = CommunityNotificationsVideo.objects.get(community=self.community)
		except:
			self.notify_video = CommunityNotificationsVideo.objects.create(community=self.community)
		return super(CommunityNotifyVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyVideoView,self).get_context_data(**kwargs)
		context["form"] = CommunityNotifyVideoForm(instance=self.notify_video, initial={"community":self.community},)
		context["notify_video"] = self.notify_video
		context["community"] = self.community
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.notify_video, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityNotificationsVideo.objects.get(community=self.community), CommunityNotifyVideoForm(request.POST, instance=self.notify_video)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyVideoView,self).post(request,*args,**kwargs)

class CommunityNotifyMusicView(TemplateView):
	template_name, form = None, None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/notify_music.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.notify_music = CommunityNotificationsMusic.objects.get(community=self.community)
		except:
			self.notify_music = CommunityNotificationsMusic.objects.create(community=self.community)
		return super(CommunityNotifyMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityNotifyMusicView,self).get_context_data(**kwargs)
		context["form"] = CommunityNotifyMusicForm(instance=self.notify_music, initial={"community":self.community},)
		context["community"] = self.community
		context["notify_music"] = self.notify_music
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.notify_music, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityNotificationsMusic.objects.get(community=self.community), CommunityNotifyMusicForm(request.POST, instance=self.notify_music)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse ('!')
		return super(CommunityNotifyMusicView,self).post(request,*args,**kwargs)

class CommunityPrivatePostView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/private_post.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.private_post = CommunityPrivatePost.objects.get(community=self.community)
		except:
			self.private_post = CommunityPrivatePost.objects.create(community=self.community)
		return super(CommunityPrivatePostView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivatePostView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = CommunityPrivatePostForm(instance=self.private_post)
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.private_post, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityPrivatePost.objects.get(community=self.community), CommunityPrivatePostForm(request.POST, instance=self.private_post)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateGoodView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/private_good.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.private_good = CommunityPrivateGood.objects.get(community=self.community)
		except:
			self.private_good = CommunityPrivateGood.objects.create(community=self.community)
		return super(CommunityPrivateGoodView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivateGoodView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = CommunityPrivateGoodForm(instance=self.private_good)
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.private_good, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityPrivateGood.objects.get(community=self.community), CommunityPrivateGoodForm(request.POST, instance=self.private_good)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateVideoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/private_video.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.private_video = CommunityPrivateVideo.objects.get(community=self.community)
		except:
			self.private_video = CommunityPrivateVideo.objects.create(community=self.community)
		return super(CommunityPrivateVideoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivateVideoView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = CommunityPrivateVideoForm(instance=self.private_video)
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.private_video, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityPrivateVideo.objects.get(community=self.community), CommunityPrivateVideoForm(request.POST, instance=self.private_video)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivatePhotoView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/private_photo.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.private_photo = CommunityPrivatePhoto.objects.get(community=self.community)
		except:
			self.private_photo = CommunityPrivatePhoto.objects.create(community=self.community)
		return super(CommunityPrivatePhotoView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivatePhotoView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = CommunityPrivatePhotoForm(instance=self.private_photo)
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.private_photo, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityPrivatePhoto.objects.get(community=self.community), CommunityPrivatePhotoForm(request.POST, instance=self.private_photo)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityPrivateMusicView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/private_music.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		try:
			self.private_music = CommunityPrivateMusic.objects.get(community=self.community)
		except:
			self.private_music = CommunityPrivateMusic.objects.create(community=self.community)
		return super(CommunityPrivateMusicView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPrivateMusicView,self).get_context_data(**kwargs)
		context["community"] = self.community
		context["form"] = CommunityPrivateMusicForm(instance=self.private_music)
		return context

	def post(self,request,*args,**kwargs):
		self.community, self.private_music, self.form = Community.objects.get(pk=self.kwargs["pk"]), CommunityPrivateMusic.objects.get(community=self.community), CommunityPrivateMusicForm(request.POST, instance=self.private_music)
		if self.form.is_valid() and request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
			self.form.save()
			return HttpResponse()

class CommunityAdminView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/admins.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityAdminView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityAdminView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		admins = self.community.get_community_administrators(self.community.pk)
		return admins


class CommunityEditorsView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/editors.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityEditorsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityEditorsView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		admins = self.community.get_community_editors(self.community.pk)
		return admins


class CommunityAdvertisersView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/advertisers.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityAdvertisersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityAdvertisersView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		advertisers = self.community.get_community_advertisers(self.community.pk)
		return advertisers


class CommunityModersView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/moders.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityModersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityModersView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		moders=self.community.get_community_moderators(self.community.pk)
		return moders


class CommunityBlackListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_moders_template("communities/manage/moders.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityBlackListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityBlackListView,self).get_context_data(**kwargs)
		context["community"]=self.community
		return context

	def get_queryset(self):
		black_list=self.community.get_community_banned_users(self.community.pk)
		return black_list


class CommunityFollowsView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("communities/manage/follows.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
		return super(CommunityFollowsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityFollowsView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		from follows.models import CommunityFollow

		follows = CommunityFollow.get_community_follows(self.community.pk)
		return follows


class CommunityMemberManageView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.community,
		self.administrators,
		self.moderators,
		self.editors,
		self.advertisers,
		self.template_name = Community.objects.get(pk=self.kwargs["pk"]), Community.get_community_administrators(self.community.pk),Community.get_community_moderators(self.community.pk),Community.get_community_editors(self.community.pk),Community.get_community_advertisers(self.community.pk),get_community_manage_template("communities/manage/members.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
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
		from users.models import User

		self.community, self.user, self.administrator, self.moderator, self.editor, self.advertiser, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), \
		User.objects.get(uuid=self.kwargs["uuid"]), self.user.is_administrator_of_community(self.community.pk), self.user.is_moderator_of_community(self.community.pk), \
		self.user.is_editor_of_community(self.community.pk), self.user.is_advertiser_of_community(self.community.pk), get_community_manage_template("communities/manage/staff_window.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
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
