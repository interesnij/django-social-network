from django.views.generic.base import TemplateView
from users.models import User
from survey.models import Survey, Answer, SurveyList
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.user import check_user_can_get_list
from common.templates import get_settings_template, render_for_platform, get_detect_platform_template


class SurveyUserCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("survey/user/add.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from survey.forms import SurveyForm
        context = super(SurveyUserCreate,self).get_context_data(**kwargs)
        context["form"] = SurveyForm()
        return context

    def post(self,request,*args,**kwargs):
        from survey.forms import SurveyForm

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.form = SurveyForm(request.POST,request.FILES)
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
                                            community=None,
                                            )
            return render_for_platform(request, 'survey/user/preview.html',{'object': new_survey})
        else:
            return HttpResponseBadRequest("")


class SurveyUserEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.survey = Survey.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_detect_platform_template("survey/user/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyUserEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from survey.forms import SurveyForm
        context = super(SurveyUserEdit,self).get_context_data(**kwargs)
        context["survey"] = self.survey
        context["form_post"] = SurveylistForm(instance=self.survey)
        return context

    def post(self,request,*args,**kwargs):
        from survey.forms import SurveyForm
        self.survey, self.form = Survey.objects.get(pk=self.kwargs["pk"]), SurveyForm(request.POST,request.FILES,instance=self.survey)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == survey.creator.pk:
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
        return super(SurveyUserEdit,self).get(request,*args,**kwargs)


class SurveyUserDelete(View):
    def get(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == survey.creator.pk:
            survey.delete_item()
            return HttpResponse()
        else:
            raise Http404

class SurveyUserRecover(View):
    def get(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == survey.creator.pk:
            survey.restore_item()
            return HttpResponse()
        else:
            raise Http404


class UserSurveyVote(View):
    def get(self, request, **kwargs):
        answer = Answer.objects.get(pk=self.kwargs["survey_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return answer.vote(request.user, None)


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


class AddSurveyListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.add_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemoveSurveyListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class UserSurveyListCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("survey/user/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserSurveyListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from survey.forms import SurveylistForm
        context = super(UserSurveyListCreate,self).get_context_data(**kwargs)
        context["form_post"] = SurveylistForm()
        return context

    def post(self,request,*args,**kwargs):
        from survey.forms import SurveylistForm
        form_post, user = SurveylistForm(request.POST), User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and form_post.is_valid():
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=None)
            return render_for_platform(request, 'users/user_survey_list/my_list.html',{'list': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()

class UserSurveyListEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list, self.template_name = get_settings_template("survey/user/edit_list.html", request.user, request.META['HTTP_USER_AGENT']), SurveyList.objects.get(uuid=self.kwargs["uuid"])
        return super(UserSurveyListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from survey.forms import SurveylistForm
        context = super(UserSurveyListEdit,self).get_context_data(**kwargs)
        context["list"] = self.list
        context["form"] = SurveylistForm(instance=self.list)
        return context

    def post(self,request,*args,**kwargs):
        from survey.forms import SurveylistForm
        self.list = SurveyList.objects.get(pk=self.kwargs["pk"])
        self.form = SurveylistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.list.creator.pk:
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description, community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserSurveyListEdit,self).get(request,*args,**kwargs)

class UserSurveyListDelete(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == list.creator.pk and list.type != SurveyList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserSurveyListRecover(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == list.creator.pk:
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class UserChangeSurveyPosition(View):
    def post(self,request,*args,**kwargs):
        import json

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                post = Survey.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class UserChangeSurveyListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from users.model.list import UserSurveyListPosition

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                list = UserSurveyListPosition.objects.get(list=item['key'], user=user.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()
