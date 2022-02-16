from survey.models import SurveyList, Survey
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
								get_settings_template,
								render_for_platform
							)

class SurveyView(ListView):
	template_name = "survey.html"

	def get_queryset(self):
		return Survey.objects.only("pk")


class LoadSurveyList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = SurveyList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_list(self.list, "survey/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_list(self.list, "survey/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_list(self.list, "survey/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_list(self.list, "survey/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadSurveyList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadSurveyList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()


class AddSurveyInList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("survey/add.html", request.user, request.META['HTTP_USER_AGENT'])
		self.list = SurveyList.objects.get(pk=self.kwargs["pk"])
		return super(AddSurveyInList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from survey.forms import SurveyForm
		context = super(AddSurveyInList,self).get_context_data(**kwargs)
		context["form"] = SurveyForm()
		context["list"] = self.list
		return context

	def post(self,request,*args,**kwargs):
		from survey.forms import SurveyForm

		list = SurveyList.objects.get(pk=self.kwargs["pk"])
		self.form = SurveyForm(request.POST,request.FILES)
		if request.is_ajax() and self.form.is_valid() and list.is_user_can_create_el(request.user.pk):
			survey = self.form.save(commit=False)
			answers = request.POST.getlist("answers")
			if not answers:
				HttpResponse("not ansvers")
			new_survey = survey.create_survey(
					title=survey.title,
					image=survey.image,
					creator=request.user,
					list=list,
					is_anonymous=survey.is_anonymous,
					is_multiple=survey.is_multiple,
					is_no_edited=survey.is_no_edited,
					time_end=survey.time_end,
					answers=answers,
					community=list.community,
				)
			return render_for_platform(request, 'users/survey/survey.html',{'object': new_survey})
		else:
			return HttpResponseBadRequest()


class SurveyEdit(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.survey = Survey.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("survey/edit.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(SurveyEdit,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from survey.forms import SurveyForm
		context = super(SurveyEdit,self).get_context_data(**kwargs)
		context["survey"] = self.survey
		context["form_post"] = SurveyForm(instance=self.survey)
		return context

	def post(self,request,*args,**kwargs):
		from survey.forms import SurveyForm

		survey = Survey.objects.get(pk=self.kwargs["pk"])
		form = SurveyForm(request.POST, request.FILES, instance=survey)
		if request.is_ajax() and form.is_valid() and \
		survey.list.is_user_can_create_el(request.user.pk)\
		and survey.is_can_edit():
			survey = form.save(commit=False)
			answers = request.POST.getlist("answers")
			if not answers:
				HttpResponse("not ansvers")
			new_survey = survey.edit_survey(
				title=survey.title,
				image=survey.image,
				is_anonymous=survey.is_anonymous,
				is_multiple=survey.is_multiple,
				is_no_edited=survey.is_no_edited,
				time_end=survey.time_end,
				answers=answers,
			)
			return HttpResponse()
		else:
			return HttpResponseBadRequest()


class SurveyDelete(View):
	def get(self, request, *args, **kwargs):
		survey = Survey.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and survey.is_user_can_edit_delete_item(request.user):
			survey.delete_item()
		return HttpResponse()

class SurveyRecover(View):
	def get(self, request, *args, **kwargs):
		survey = Survey.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and survey.is_user_can_edit_delete_item(request.user):
			survey.restore_item()
		return HttpResponse()


class SurveyVote(View):
	def post(self, request, **kwargs):
		survey = Survey.objects.get(pk=self.kwargs["pk"])
		answers = request.POST.getlist("votes")
		if survey.list.is_user_can_see_el(request.user.pk):
			return survey.votes_create(request.user, answers)
		return HttpResponse()

class SurveyUnVote(View):
	def get(self, request, **kwargs):
		survey = Survey.objects.get(pk=self.kwargs["pk"])
		if survey.list.is_user_can_see_el(request.user.pk):
			return survey.votes_delete(request.user)
		return HttpResponse()


class SurveyDetail(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.survey = Survey.objects.get(pk=self.kwargs["pk"])
		if self.survey.list.is_user_can_see_el(request.user.pk):
			self.template_name = get_settings_template("survey/survey.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(SurveyDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(SurveyDetail,self).get_context_data(**kwargs)
		context["object"] = self.survey
		return context

class SurveyVoters(ListView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.survey = Survey.objects.get(pk=self.kwargs["pk"])
		if (not self.survey.is_anonymous \
		or not self.survey.type[0] != "_") \
		and self.survey.list.is_user_can_see_el(request.user.pk):
			self.template_name = get_settings_template("survey/voters.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(SurveyVoters,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(SurveyVoters,self).get_context_data(**kwargs)
		context["survey"] = self.survey
		return context

	def get_queryset(self):
		return self.survey.get_users()
