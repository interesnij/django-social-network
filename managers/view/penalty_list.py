from users.models import User
from django.views.generic import ListView
from django.http import Http404
from common.templates import get_staff_template


class PenaltyUserList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_user_manager():
            self.template_name = get_staff_template("managers/penalty_list/user_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyUserList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_penalty_users()
        return list

class PenaltyCommunityList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_community_manager():
            self.template_name = get_staff_template("managers/penalty_list/community_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyCommunityList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_penalty_communities()
        return list

class PenaltyPostsList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_post_manager():
            self.template_name = get_staff_template("managers/penalty_list/post_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyPostsList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_penalty_posts()
        return list


class PenaltyPhotoList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_photo_administrator():
            self.template_name = get_staff_template("managers/penalty_list/photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyPhotoList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_penalty_photos()
        return list


class PenaltyGoodList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_good_manager():
            self.template_name = get_staff_template("managers/penalty_list/good_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyGoodList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_penalty_goods()
        return list


class PenaltyAudioList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_audio_manager():
            self.template_name = get_staff_template("managers/penalty_list/audio_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyAudioList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_penalty_audios()
        return list


class PenaltyVideoList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_video_manager():
            self.template_name = get_staff_template("managers/penalty_list/video_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyVideoList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        list = self.user.get_penalty_videos()
        return list


class PenaltyDocList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_doc_manager():
            self.template_name = get_staff_template("managers/penalty_list/doc_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyDocList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class PenaltyPlannerList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_planner_manager():
            self.template_name = get_staff_template("managers/penalty_list/planner_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyPlannerList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class PenaltySiteList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_site_manager():
            self.template_name = get_staff_template("managers/penalty_list/site_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltySiteList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class PenaltyWikiList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_wiki_manager():
            self.template_name = get_staff_template("managers/penalty_list/wiki_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyWikiList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class PenaltyForumList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_forum_manager():
            self.template_name = get_staff_template("managers/penalty_list/forum_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyForumList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class PenaltyArticleList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_article_manager():
            self.template_name = get_staff_template("managers/penalty_list/article_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyArticleList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class PenaltySurveyList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_survey_manager():
            self.template_name = get_staff_template("managers/penalty_list/survey_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltySurveyList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class PenaltyMailList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_mail_manager():
            self.template_name = get_staff_template("managers/penalty_list/mail_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyMailList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []

class PenaltyMessageList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        if self.user.is_message_manager():
            self.template_name = get_staff_template("managers/penalty_list/message_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PenaltyMessageList,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return []
