from users.models import User
from django.views.generic import ListView


class PenaltyUserAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/user_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyUserAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyUserAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_users()
        return list

class PenaltyCommunityAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/community_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyCommunityAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyCommunityAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_communities()
        return list

class PenaltyPostAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/post_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyPostAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPostAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyPhotoAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/photo_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyPhotoAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPhotoAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyGoodAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/good_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyGoodAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyGoodAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyAudioAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/audio_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyAudioAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyAudioAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyVideoAdminList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/video_admin_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyVideoAdminList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyVideoAdminList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class PenaltyUserEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_editor or self.user.is_superuser:
            self.template_name = "penalty_list/user_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyUserEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyUserEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_users()
        return list

class PenaltyCommunityEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_editor or self.user.is_superuser:
            self.template_name = "penalty_list/community_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyCommunityEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyCommunityEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_communities()
        return list

class PenaltyPostEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_editor or self.user.is_superuser:
            self.template_name = "penalty_list/post_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyPostEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPostEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyPhotoEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_editor or self.user.is_superuser:
            self.template_name = "penalty_list/photo_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyPhotoEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPhotoEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyGoodEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_editor or self.user.is_superuser:
            self.template_name = "penalty_list/good_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyGoodEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyGoodEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyAudioEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_editor or self.user.is_superuser:
            self.template_name = "penalty_list/audio_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyAudioEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyAudioEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyVideoEditorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_editor or self.user.is_superuser:
            self.template_name = "penalty_list/video_editor_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyVideoEditorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyVideoEditorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class PenaltyUserModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_moderator or self.user.is_superuser:
            self.template_name = "penalty_list/user_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyUserModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyUserModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_users()
        return list

class PenaltyCommunityModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_moderator or self.user.is_superuser:
            self.template_name = "penalty_list/community_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyCommunityModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyCommunityModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_communities()
        return list

class PenaltyPostModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_moderator or self.user.is_superuser:
            self.template_name = "penalty_list/post_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyPostModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPostModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyPhotoModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_moderator or self.user.is_superuser:
            self.template_name = "penalty_list/photo_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyPhotoModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPhotoModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyGoodModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_moderator or self.user.is_superuser:
            self.template_name = "penalty_list/good_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyGoodModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyGoodModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyAudioModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_moderator or self.user.is_superuser:
            self.template_name = "penalty_list/audio_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyAudioModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyAudioModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyVideoModeratorList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_moderator or self.user.is_superuser:
            self.template_name = "penalty_list/video_moderator_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyVideoModeratorList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyVideoModeratorList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyUserAdvertiserList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_advertiser or self.user.is_superuser:
            self.template_name = "penalty_list/user_advertiser_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyUserAdvertiserList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyUserAdvertiserList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class PenaltyCommunityAdvertiserList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_advertiser or self.user.is_superuser:
            self.template_name = "penalty_list/community_advertiser_list.html"
        else:
            self.template_name = "about.html"
        return super(PenaltyCommunityAdvertiserList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyCommunityAdvertiserList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list
