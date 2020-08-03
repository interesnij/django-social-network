from users.models import User
from django.views.generic import ListView
from django.http import Http404


class PenaltyUserList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_manager or self.user.is_superuser:
            self.template_name = "penalty_list/user_list.html"
        else:
            raise Http404
        return super(PenaltyUserList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyUserList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_users()
        return list

class PenaltyCommunityList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_community_manager or self.user.is_superuser:
            self.template_name = "penalty_list/community_list.html"
        else:
            raise Http404
        return super(PenaltyCommunityList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyCommunityList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_communities()
        return list

class PenaltyPostList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_manager or self.user.is_superuser:
            self.template_name = "penalty_list/post_list.html"
        else:
            raise Http404
        return super(PenaltyPostList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPostList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_posts()
        return list

class PenaltyPostCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_post_manager or self.user.is_superuser:
            self.template_name = "penalty_list/post_comment_list.html"
        else:
            raise Http404
        return super(PenaltyPostCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPostCommentList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_post_comments()
        return list


class PenaltyPhotoList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/photo_list.html"
        else:
            raise Http404
        return super(PenaltyPhotoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPhotoList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_photos()
        return list

class PenaltyPhotoCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_photo_administrator or self.user.is_superuser:
            self.template_name = "penalty_list/photo_comment_list.html"
        else:
            raise Http404
        return super(PenaltyPhotoCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyPhotoCommentList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_photo_comments()
        return list


class PenaltyGoodList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_manager or self.user.is_superuser:
            self.template_name = "penalty_list/good_list.html"
        else:
            raise Http404
        return super(PenaltyGoodList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyGoodList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_goods()
        return list

class PenaltyGoodCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_good_manager or self.user.is_superuser:
            self.template_name = "penalty_list/good_comment_list.html"
        else:
            raise Http404
        return super(PenaltyGoodCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyGoodCommentList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_good_comments()
        return list


class PenaltyAudioList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_audio_manager or self.user.is_superuser:
            self.template_name = "penalty_list/audio_list.html"
        else:
            raise Http404
        return super(PenaltyAudioList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyAudioList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_audios()
        return list


class PenaltyVideoList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_manager or self.user.is_superuser:
            self.template_name = "penalty_list/video_list.html"
        else:
            raise Http404
        return super(PenaltyVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyVideoList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_videos()
        return list

class PenaltyVideoCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_video_manager or self.user.is_superuser:
            self.template_name = "penalty_list/video_comment_list.html"
        else:
            raise Http404
        return super(PenaltyVideoCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyVideoCommentList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = self.user.get_penalty_video_comments()
        return list

class PenaltyUserAdvertiserList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_advertiser or self.user.is_superuser:
            self.template_name = "penalty_list/user_advertiser_list.html"
        else:
            raise Http404
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
            raise Http404
        return super(PenaltyCommunityAdvertiserList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PenaltyCommunityAdvertiserList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        list = []
        return list
