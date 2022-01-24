from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post, PostsList
from survey.models import Survey, SurveyList
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists


class UUCMSurveyWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.survey, self.template_name = Survey.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("survey/repost/u_ucm_survey.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.survey.list.is_user_can_copy_el(request.user.pk)
        if self.survey.creator != request.user:
            check_user_can_get_list(request.user, self.survey.creator)
        return super(UUCMSurveyWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMSurveyWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.survey, self.can_copy_item
        return c

class CUCMSurveyWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.survey, self.template_name = Survey.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("survey/repost/c_ucm_survey.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.survey.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.survey.community)
        return super(CUCMSurveyWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMSurveyWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.survey, self.survey.community, self.can_copy_item
        return c


class UUCMSurveyListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.list, self.template_name = SurveyList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("survey/repost/u_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        if self.list.creator != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMSurveyListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMSurveyListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.list, self.can_copy_item
        return c

class CUCMSurveyListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.list, self.template_name = SurveyList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("survey/repost/c_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.list.community)
        return super(CUCMSurveyListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMSurveyListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.list, self.list.community, self.can_copy_item
        return c


class UUSurveyRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        survey, form_post, attach, lists, count, creator = Survey.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if survey.creator.pk != creator.pk:
            check_user_can_get_list(creator, survey.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=survey.creator, community=None, attach="sur"+str(survey.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "SUR", "create_u_survey_notify", "RE")
                user_wall(creator, None, parent.pk, "SUR", "create_u_survey_wall", "RE")

            survey.repost += count
            survey.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUSurveyRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        survey, form_post, attach, lists, count, creator = Survey.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, survey.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=survey.creator, community=survey.community, attach="sur"+str(survey.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "SUR", "create_c_survey_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "SUR", "create_c_survey_wall", "RE")

            survey.repost += count
            survey.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCSurveyRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        survey, form_post, attach, lists, count, creator = Survey.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if survey.creator.pk != creator.pk:
            check_user_can_get_list(creator, survey.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=survey.creator, community=None, attach="sur"+str(survey.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community.pk, parent.pk, "SUR", "create_u_survey_notify", "CR")
                    user_wall(creator, community.pk, parent.pk, "SUR", "create_u_survey_wall", "CR")

            survey.repost += count
            survey.save(update_fields=["repost"])
        return HttpResponse()


class CCSurveyRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        survey, form_post, attach, lists, count, creator = Survey.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, survey.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=survey.creator, community=survey.community, attach="sur"+str(survey.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "SUR", "create_c_survey_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "SUR", "create_c_survey_wall", "CR")

            survey.repost += count
            survey.save(update_fields=["repost"])
        return HttpResponse()


class UMSurveyRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if survey.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, user)
        repost_message_send(survey, "sur"+str(survey.pk), None, request)

        return HttpResponse()


class CMSurveyRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        survey = Survey.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, survey.community)
        repost_message_send(survey, "sur"+str(survey.pk), survey.community, request)
        return HttpResponse()


class UUSurveyListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        list, form_post, attach, lists, count, creator = SurveyList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if list.creator.pk != creator.pk:
            check_user_can_get_list(creator, list.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lsu"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "SUL", "create_u_survey_notify", "RE")
                user_wall(creator, None, parent.pk, "SUL", "create_u_survey_wall", "RE")

            list.repost += count
            list.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUSurveyListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        list, form_post, attach, lists, count, creator = SurveyList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, list.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="lsu"+str(list.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "SUL", "create_c_survey_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "SUL", "create_c_survey_wall", "RE")

            list.repost += count
            list.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCSurveyListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        list, form_post, attach, lists, count, creator = SurveyList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if list.creator.pk != creator.pk:
            check_user_can_get_list(creator, list.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lsu"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community.pk, parent.pk, "SUL", "create_u_survey_notify", "CR")
                    user_wall(creator, community.pk, parent.pk, "SUL", "create_u_survey_wall", "CR")

            list.repost += count
            list.save(update_fields=["repost"])
        return HttpResponse()


class CCSurveyListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        list, form_post, attach, lists, count, creator = SurveyList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, list.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="lsu"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "SUL", "create_c_survey_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "SUL", "create_c_survey_wall", "CR")

            list.repost += count
            list.save(update_fields=["repost"])
        return HttpResponse()


class UMSurveyListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        if list.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, user)
        repost_message_send(list, "lsu"+str(list.pk), None, request)

        return HttpResponse()


class CMSurveyListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, list.community)
        repost_message_send(list, "lsu"+str(list.pk), list.community, request)
        return HttpResponse()
