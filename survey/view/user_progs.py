from django.views.generic.base import TemplateView
from users.models import User
from survey.models import Survey
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.user import check_user_can_get_list
from survey.forms import SurveyForm
from notify.model.survey import *
from common.template.user import get_settings_template, render_for_platform, get_detect_platform_template
from datetime import datetime


class SurveyUserCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("survey/user/add.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SurveyUserCreate,self).get_context_data(**kwargs)
        context["form"] = SurveyForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form = SurveyForm(request.POST,request.FILES)
        if request.is_ajax() and self.form.is_valid():
            survey = self.form.save(commit=False)
            answers = request.POST.getlist("answers")
            if not answers:
                HttpResponse("not ansvers")
            new_survey = survey.create_survey(
                                            title=survey.title,
                                            creator=request.user,
                                            community=None,
                                            order=survey.order,
                                            is_anonymous=survey.is_anonymous,
                                            is_multiple=survey.is_multiple,
                                            is_no_edited=survey.is_no_edited,
                                            time_end=survey.time_end,
                                            answers=answers)
            for ansver in answers:
                Answer.objects.create(survey=new_survey, text=ansver)
            return render_for_platform(request, 'survey/user/new_survey.html',{'object': new_survey})
        else:
            return HttpResponseBadRequest("")


class SurveyUserEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("survey/user/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyUserEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SurveyUserEdit,self).get_context_data(**kwargs)
        context["survey"] = Survey.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.survey, self.form = Survey.objects.get(pk=self.kwargs["pk"]), SurveyForm(request.POST,request.FILES,instance=self.survey)
        if request.is_ajax() and self.form.is_valid():
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(SurveyUserEdit,self).get(request,*args,**kwargs)


class SurveyUserDelete(View):
    def get(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == survey.creator.pk:
            survey.is_deleted = True
            survey.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class SurveyUserAbortDelete(View):
    def get(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == survey.creator.pk:
            survey.is_deleted = False
            survey.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404


class UserSurveyVote(View):
    def get(self, request, **kwargs):
        answer = Answer.objects.get(pk=self.kwargs["survey_pk"])
        user, survey = User.objects.get(pk=self.kwargs["pk"]), answer.survey
        if survey.time_end < datetime.now():
            return HttpResponse()
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            answer = SurveyVote.objects.get(answer=answer, user=request.user)
            if survey.is_no_edited:
                return HttpResponse()
            else:
                answer.delete()
                result = True
        except SurveyVote.DoesNotExist:
            if not survey.is_multiple and request.user.is_voted_of_survey(survey.pk):
                request.user.get_vote_of_survey(survey.pk).delete()
            SurveyVote.objects.create(answer=answer, user=request.user)
            result = True
            if user.pk != request.user.pk:
                if survey.is_anonymous:
                    answer_notification_handler(request.user, survey.creator, survey, SurveyNotify.ANON_VOTE)
                else:
                    answer_notification_handler(request.user, survey.creator, survey, SurveyNotify.VOTE)
        return HttpResponse(json.dumps({"result": result,"votes": survey.get_votes_count()}), content_type="application/json")


class SurveyUserDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.survey = Survey.objects.get(pk=self.kwargs["survey_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_detect_platform_template("survey/user/survey.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyUserDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SurveyUserDetail,self).get_context_data(**kwargs)
        context["object"] = self.survey
        context["user"] = self.user
        return context
