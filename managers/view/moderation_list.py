from users.models import User
from django.views.generic import ListView


class ModerationUserList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_manager or self.user.is_superuser:
            self.template_name = "moderation_list/user_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationUserList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationUserList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_users()
        return list

class ModerationCommunityList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_manager or self.user.is_superuser:
            self.template_name = "moderation_list/community_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationCommunityList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationCommunityList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_communities()
        return list

class ModerationPostList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_manager or self.user.is_superuser:
            self.template_name = "moderation_list/post_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPostList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPostList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_posts()
        return list

class ModerationPostCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_manager or self.user.is_superuser:
            self.template_name = "moderation_list/post_comment_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPostCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPostCommentList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_moderation_post_comments()
        return list


class ModerationPhotoList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_manager or self.user.is_superuser:
            self.template_name = "moderation_list/photo_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPhotoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPhotoList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationPhotoCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_manager or self.user.is_superuser:
            self.template_name = "moderation_list/photo_comment_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationPhotoCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationPhotoCommentList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class ModerationGoodList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_manager or self.user.is_superuser:
            self.template_name = "moderation_list/good_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationGoodList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationGoodList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationGoodCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_manager or self.user.is_superuser:
            self.template_name = "moderation_list/good_comment_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationGoodCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationGoodCommentList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class ModerationAudioList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_manager or self.user.is_superuser:
            self.template_name = "moderation_list/audio_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationAudioList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationAudioList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list


class ModerationVideoList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_manager or self.user.is_superuser:
            self.template_name = "moderation_list/video_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationVideoList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list

class ModerationVideoCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_manager or self.user.is_superuser:
            self.template_name = "moderation_list/video_comment_list.html"
        else:
            self.template_name = "about.html"
        return super(ModerationVideoCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ModerationVideoCommentList,self).get_context_data(**kwargs)
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
