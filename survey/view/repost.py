from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from survey.models import SurveyList, Survey
from users.models import User
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.processing.post import repost_message_send
from common.templates import get_detect_platform_template


class UUCMSurveyWindow(TemplateView):
    """
    форма репоста опроса пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.survey, self.template_name = Survey.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("survey/repost/u_ucm_survey.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.survey.list.is_user_can_copy_el(request.user.pk)
        if self.survey.creator != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMSurveyWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMSurveyWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.survey
        context["can_copy_item"] = self.can_copy_item
        return context

class CUCMSurveyWindow(TemplateView):
    """
    форма репоста опроса сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.survey, self.template_name = Survey.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/c_ucm_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.survey.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.survey.community)
        return super(CUCMSurveyWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMSurveyWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.survey
        context["community"] = self.survey.community
        context["can_copy_item"] = self.can_copy_item
        return context

class UUCMSurveyListWindow(TemplateView):
    """
    форма репоста списка опросов пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list, self.template_name = SurveyList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/u_ucm_list_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        if self.list.creator != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMSurveyListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMSurveyListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.list
        context["can_copy_item"] = self.can_copy_item
        return context

class CUCMSurveyListWindow(TemplateView):
    """
    форма репоста списка опросов сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list, self.template_name = SurveyList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/c_ucm_list_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.list.community)
        return super(CUCMSurveyListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMSurveyListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.list
        context["community"] = self.list.community
        context["can_copy_item"] = self.can_copy_item
        return context


class UUSurveyRepost(View):
    """
    создание репоста опроса пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        survey, form_post, attach = Survey.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        if survey.creator != request.user:
            check_user_can_get_list(request.user, survey.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=user, community=None, attach="survey"+str(survey.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent, community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUSurveyRepost(View):
    """
    создание репоста опроса сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        survey, form_post, attach = Survey.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, survey.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=request.user, community=survey.community, attach="survey"+str(survey.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent, community=None)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCSurveyRepost(View):
    """
    создание репоста опроса пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if survey.creator != request.user:
            check_user_can_get_list(request.user, survey.creator)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, attach="survey"+str(survey.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class CCSurveyRepost(View):
    """
    создание репоста опроса сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, survey.community)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=survey.community, attach="survey"+str(survey.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMSurveyRepost(View):
    """
    создание репоста опроса пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(survey, "survey"+str(survey.pk), None, request)
        return HttpResponse()


class CMSurveyRepost(View):
    """
    создание репоста опроса сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, survey.community)
        repost_message_send(survey, "survey"+str(survey.pk), None, survey.community)
        return HttpResponse()


class UUSurveyListRepost(View):
    """
    создание репоста списка опросов пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        list, form_post, attach = SurveyList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        if list.creator != request.user:
            check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="ldo"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, is_signature=False, attach=attach, text=post.text, comments_enabled=post.comments_enabled, parent=parent, community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUSurveyListRepost(View):
    """
    создание репоста списка опросов сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        list, form_post, attach = SurveyList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, list.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="lsu"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent,community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCSurveyListRepost(View):
    """
    создание репоста списка опросов пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        if list.creator != request.user:
            check_user_can_get_list(request.user, list.creator)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, attach="lsu"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()

class CCSurveyListRepost(View):
    """
    создание репоста списка опросов сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, list.community)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, attach="lsu"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMSurveyListRepost(View):
    """
    создание репоста списка опросов пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        if list.creator != request.user:
            check_user_can_get_list(request.user, list.creator)
        repost_message_send(list, "lsu"+str(list.pk), None, request)
        return HttpResponse()


class CMSurveyListRepost(View):
    """
    создание репоста списка опросов сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, list.community)
        repost_message_send(list, "lsu"+str(list.pk), list.community, request)
        return HttpResponse()
