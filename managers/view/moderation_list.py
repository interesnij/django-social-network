from users.models import User
from django.views.generic import ListView
from django.http import Http404
from common.template.user import get_detect_platform_template


class ModerationUserList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_user_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/user_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationUserList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_users()
        return list

class ModerationCommunityList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_community_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/community_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationCommunityList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_communities()
        return list

class ModerationPostList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_post_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/post_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPostList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_posts()
        return list

class ModerationPostCommentList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_post_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/post_comment_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPostCommentList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_post_comments()
        return list


class ModerationPhotoList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_photo_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPhotoList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_photos()
        return list

class ModerationPhotoCommentList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_photo_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/photo_comment_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPhotoCommentList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_photo_comments()
        return list


class ModerationGoodList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_good_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/good_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationGoodList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_goods()
        return list

class ModerationGoodCommentList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_good_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/good_comment_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationGoodCommentList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_good_comments()
        return list


class ModerationAudioList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_audio_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/audio_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationAudioList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_audios()
        return list


class ModerationVideoList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_video_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/video_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationVideoList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_videos()
        return list

class ModerationVideoCommentList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_video_manager() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/video_comment_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationVideoCommentList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_video_comments()
        return list


class ModerationUserAdvertiserList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_user_advertiser() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/user_advertiser_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationUserAdvertiserList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = []
        return list

class ModerationCommunityAdvertiserList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_community_advertiser() or self.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/moderation_list/community_advertiser_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationCommunityAdvertiserList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = []
        return list
