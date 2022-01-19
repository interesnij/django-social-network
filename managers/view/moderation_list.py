from users.models import User
from django.views.generic import ListView
from django.http import Http404
from common.templates import get_staff_template


class ModerationUserList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/user_list.html", request.user, request.META['HTTP_USER_AGENT'])
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
        if self.user.is_manager():
            self.template_name = get_detect_platform_template("managers/moderation_list/community_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationCommunityList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_staff_template()
        return list

class ModerationPostsList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/post_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPostsList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_posts()
        return list

class ModerationPhotoList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPhotoList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_photos()
        return list


class ModerationGoodList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/good_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationGoodList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_goods()
        return list


class ModerationAudioList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/audio_list.html", request.user, request.META['HTTP_USER_AGENT'])
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
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/video_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationVideoList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_moderation_videos()
        return list

class ModerationDocList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/doc_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationDocList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationPlannerList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/planner_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationPlannerList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationSiteList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/site_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationSiteList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationWikiList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/wiki_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationWikiList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationForumList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/forum_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationForumList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationArticleList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/article_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationArticleList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationSurveyList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/survey_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationSurveyList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationMailList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/mail_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationMailList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class ModerationMessageList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_manager():
            self.template_name = get_staff_template("managers/moderation_list/message_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ModerationMessageList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []
