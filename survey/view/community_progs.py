from django.views.generic.base import TemplateView
from communities.models import Community
from survey.models import Survey, Answer, SurveyList
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.community import check_can_get_lists
from common.templates import get_detect_platform_template, render_for_platform


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
                                            list=survey.list,
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
                                            list=survey.list,
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
            survey.delete_item()
            return HttpResponse()
        else:
            raise Http404

class SurveyCommunityRecover(View):
    def get(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["survey_pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            survey.restore_item()
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
