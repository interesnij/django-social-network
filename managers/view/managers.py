from users.models import User
from django.views.generic import ListView


class UserAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_administrator or self.user.is_superuser:
            self.template_name = "manager/user_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(UserAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class CommunityAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_administrator or self.user.is_superuser:
            self.template_name = "manager/community_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(CommunityAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PostAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_administrator or self.user.is_superuser:
            self.template_name = "manager/post_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PostAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PhotoAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_administrator or self.user.is_superuser:
            self.template_name = "manager/photo_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PhotoAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class GoodAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_administrator or self.user.is_superuser:
            self.template_name = "manager/good_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(GoodAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class AudioAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_administrator or self.user.is_superuser:
            self.template_name = "manager/audio_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(AudioAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AudioAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class VideoAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_administrator or self.user.is_superuser:
            self.template_name = "manager/video_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(VideoAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class UserEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_editor or self.user.is_superuser:
            self.template_name = "manager/user_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(UserEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class CommunityEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_editor or self.user.is_superuser:
            self.template_name = "manager/community_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(CommunityEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PostEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_editor or self.user.is_superuser:
            self.template_name = "manager/post_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PostEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PhotoEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_editor or self.user.is_superuser:
            self.template_name = "manager/photo_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PhotoEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class GoodEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_editor or self.user.is_superuser:
            self.template_name = "manager/good_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(GoodEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class AudioEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_editor or self.user.is_superuser:
            self.template_name = "manager/audio_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(AudioEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AudioEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class VideoEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_editor or self.user.is_superuser:
            self.template_name = "manager/video_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(VideoEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class UserModeratorList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_moderator or self.user.is_superuser:
            self.template_name = "manager/user_moderator_list.html"
        else:
            self.template_name = "about.html"
		return super(UserModeratorList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserModeratorList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		users = []
		return users

class CommunityModeratorList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_moderator or self.user.is_superuser:
            self.template_name = "manager/community_moderator_list.html"
        else:
            self.template_name = "about.html"
		return super(CommunityModeratorList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityModeratorList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		communities = []
		return communities

class PostModeratorList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_moderator or self.user.is_superuser:
            self.template_name = "manager/post_moderator_list.html"
        else:
            self.template_name = "about.html"
		return super(PostModeratorList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PostModeratorList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		posts = []
		return posts

class PhotoModeratorList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_moderator or self.user.is_superuser:
            self.template_name = "manager/photo_moderator_list.html"
        else:
            self.template_name = "about.html"
		return super(PhotoModeratorList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PhotoModeratorList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		photos = []
		return photos

class GoodModeratorList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_moderator or self.user.is_superuser:
            self.template_name = "manager/good_moderator_list.html"
        else:
            self.template_name = "about.html"
		return super(GoodModeratorList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GoodModeratorList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		goods = []
		return goods

class AudioModeratorList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_moderator or self.user.is_superuser:
            self.template_name = "manager/audio_moderator_list.html"
        else:
            self.template_name = "about.html"
		return super(AudioModeratorList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(AudioModeratorList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		audios = []
		return audios

class VideoModeratorList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_moderator or self.user.is_superuser:
            self.template_name = "manager/video_moderator_list.html"
        else:
            self.template_name = "about.html"
		return super(VideoModeratorList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(VideoModeratorList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		videos = []
		return videos


class UserAdvertiserList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_advertiser or self.user.is_superuser:
            self.template_name = "manager/user_advertiser_list.html"
        else:
            self.template_name = "about.html"
		return super(UserAdvertiserList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserAdvertiserList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		users = []
		return users

class CommunityAdvertiserList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_advertiser or self.user.is_superuser:
            self.template_name = "manager/community_advertiser_list.html"
        else:
            self.template_name = "about.html"
		return super(CommunityAdvertiserList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityAdvertiserList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		communities = []
		return communities
