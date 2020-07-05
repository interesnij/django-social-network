from users.models import User
from django.views.generic import ListView


class ModerationUserAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_administrator or self.user.is_superuser:
            self.template_name = "moderation_list/user_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationUserAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationUserAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_users()
        return list

class ModerationCommunityAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_administrator or self.user.is_superuser:
            self.template_name = "moderation_list/community_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationCommunityAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationCommunityAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_communities()
        return list

class ModerationPostAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_administrator or self.user.is_superuser:
            self.template_name = "moderation_list/post_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPostAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPostAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_posts()
        return list

class ModerationPhotoAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_administrator or self.user.is_superuser:
            self.template_name = "moderation_list/photo_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPhotoAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPhotoAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationGoodAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_administrator or self.user.is_superuser:
            self.template_name = "moderation_list/good_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationGoodAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationGoodAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationAudioAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_administrator or self.user.is_superuser:
            self.template_name = "moderation_list/audio_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationAudioAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationAudioAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationVideoAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_administrator or self.user.is_superuser:
            self.template_name = "moderation_list/video_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationVideoAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationVideoAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class ModerationUserEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_editor or self.user.is_superuser:
            self.template_name = "moderation_list/user_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationUserEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationUserEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_users()
        return list

class ModerationCommunityEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_editor or self.user.is_superuser:
            self.template_name = "moderation_list/community_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationCommunityEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationCommunityEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_communities()
        return list

class ModerationPostEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_editor or self.user.is_superuser:
            self.template_name = "moderation_list/post_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPostEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPostEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_posts()
        return list

class ModerationPhotoEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_editor or self.user.is_superuser:
            self.template_name = "moderation_list/photo_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPhotoEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPhotoEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationGoodEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_editor or self.user.is_superuser:
            self.template_name = "moderation_list/good_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationGoodEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationGoodEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationAudioEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_editor or self.user.is_superuser:
            self.template_name = "moderation_list/audio_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationAudioEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationAudioEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationVideoEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_editor or self.user.is_superuser:
            self.template_name = "moderation_list/video_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationVideoEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationVideoEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class ModerationUserModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_moderator or self.user.is_superuser:
            self.template_name = "moderation_list/user_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationUserModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationUserModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_users()
        return list

class ModerationCommunityModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_moderator or self.user.is_superuser:
            self.template_name = "moderation_list/community_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationCommunityModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationCommunityModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_communities()
        return list

class ModerationPostModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_moderator or self.user.is_superuser:
            self.template_name = "moderation_list/post_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPostModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPostModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_posts()
        return list

class ModerationPhotoModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_moderator or self.user.is_superuser:
            self.template_name = "moderation_list/photo_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPhotoModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPhotoModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationGoodModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_moderator or self.user.is_superuser:
            self.template_name = "moderation_list/good_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationGoodModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationGoodModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationAudioModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_moderator or self.user.is_superuser:
            self.template_name = "moderation_list/audio_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationAudioModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationAudioModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationVideoModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_moderator or self.user.is_superuser:
            self.template_name = "moderation_list/video_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationVideoModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationVideoModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationUserAdvertiserList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_advertiser or self.user.is_superuser:
            self.template_name = "moderation_list/user_advertiser_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationUserAdvertiserList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationUserAdvertiserList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationCommunityAdvertiserList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_advertiser or self.user.is_superuser:
            self.template_name = "moderation_list/community_advertiser_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationCommunityAdvertiserList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationCommunityAdvertiserList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list
