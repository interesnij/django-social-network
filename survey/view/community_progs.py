from django.views.generic.base import TemplateView
from communities.models import Community
from survey.models import Survey, Answer, SurveyList
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.community import check_can_get_lists
from common.template.user import get_detect_platform_template
from common.template.user import render_for_platform


class SurveyCommunityCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("survey/community/add.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from survey.forms import SurveyForm
        context = super(SurveyCommunityCreate,self).get_context_data(**kwargs)
        context["form"] = SurveyForm()
        return context

    def post(self,request,*args,**kwargs):
        from survey.forms import SurveyForm
        self.form = SurveyForm(request.POST,request.FILES)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid():
            survey = self.form.save(commit=False)
            answers = request.POST.getlist("answers")
            if not answers:
                HttpResponse("not ansvers")
            new_survey = survey.create_survey(
                                            title=survey.title,
                                            image=survey.image,
                                            lists=request.POST.get("list"),
                                            creator=request.user,
                                            order=survey.order,
                                            is_anonymous=survey.is_anonymous,
                                            is_multiple=survey.is_multiple,
                                            is_no_edited=survey.is_no_edited,
                                            time_end=survey.time_end,
                                            answers=answers,
                                            community=self.community,
                                            )
            return render_for_platform(request, 'survey/community/preview.html',{'object': new_survey})
        else:
            return HttpResponseBadRequest("")


class SurveyCommunityEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.survey = Survey.objects.get(pk=self.kwargs["survey_pk"])
        self.template_name = get_detect_platform_template("survey/community/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyCommunityEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from survey.forms import SurveyForm
        context = super(SurveyCommunityEdit,self).get_context_data(**kwargs)
        context["survey"] = self.survey
        context["form_post"] = SurveylistForm(instance=self.survey)
        return context

    def post(self,request,*args,**kwargs):
        from survey.forms import SurveyForm
        self.survey, self.form = Survey.objects.get(pk=self.kwargs["pk"]), SurveyForm(request.POST,request.FILES,instance=self.survey)
        if request.is_ajax() and self.form.is_valid() and request.user.is_staff_of_community(self.kwargs["pk"]):
            survey = self.form.save(commit=False)
            new_survey = survey.edit_survey(
                                            title=survey.title,
                                            image=survey.image,
                                            lists=request.POST.get("list"),
                                            order=survey.order,
                                            is_anonymous=survey.is_anonymous,
                                            is_multiple=survey.is_multiple,
                                            is_no_edited=survey.is_no_edited,
                                            time_end=survey.time_end,
                                            answers=answers,
                                            )
        else:
            return HttpResponseBadRequest()
        return super(SurveyCommunityEdit,self).get(request,*args,**kwargs)


class SurveyCommunityDelete(View):
    def get(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["survey_pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            survey.delete_survey()
            return HttpResponse()
        else:
            raise Http404

class SurveyCommunityRecover(View):
    def get(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["survey_pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            survey.restore_survey()
            return HttpResponse()
        else:
            raise Http404


class CommunitySurveyVote(View):
    def get(self, request, **kwargs):
        answer = Answer.objects.get(pk=self.kwargs["survey_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        return answer.vote(request.user, community)


class SurveyCommunityDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.survey = Survey.objects.get(pk=self.kwargs["survey_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_detect_platform_template("survey/community/survey.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyCommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SurveyCommunityDetail,self).get_context_data(**kwargs)
        context["object"] = self.survey
        context["community"] = self.community
        return context


class AddSurveyListInCommunityCollections(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_lists(request.user, list.community)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.communities.add(request.user)
        return HttpResponse()

class RemoveSurveyListFromCommunityCollections(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_lists(request.user, list.community)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.communties.remove(request.user)
        return HttpResponse()


class CommunitySurveyListCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("survey/community/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunitySurveyListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from survey.forms import SurveylistForm
        context = super(CommunitySurveyListCreate,self).get_context_data(**kwargs)
        context["form_post"] = SurveylistForm()
        return context

    def post(self,request,*args,**kwargs):
        from survey.forms import SurveylistForm
        form_post, community = SurveylistForm(request.POST), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(community.pk):
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=community,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'communities/survey_list/my_list.html',{'list': new_list, 'community': community})
        else:
            return HttpResponseBadRequest()

class CommunitySurveyListEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list, self.template_name = get_settings_template("survey/community/edit_list.html", request.user, request.META['HTTP_USER_AGENT']), SurveyList.objects.get(uuid=self.kwargs["uuid"])
        return super(CommunitySurveyListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from survey.forms import SurveylistForm
        context = super(CommunitySurveyListEdit,self).get_context_data(**kwargs)
        context["list"] = self.list
        context["form"] = SurveylistForm(instance=self.list)
        return context

    def post(self,request,*args,**kwargs):
        from survey.forms import SurveylistForm
        self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        self.form = SurveylistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.is_staff_of_community(self.list.community.pk):
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description, order=list.order, community=self.list.community,is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunitySurveyListEdit,self).get(request,*args,**kwargs)


class CommunitySurveyListDelete(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]) and list.type == DocList.LIST:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class CommunitySurveyListRecover(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            list.restore_list()
            return HttpResponse()
        else:
            raise Http404
