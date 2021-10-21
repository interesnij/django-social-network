from django.views.generic.base import TemplateView
from django.views.generic import ListView
from quan.models import Question, QuestionsCategory
from common.templates import get_default_template


class QuanView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_default_template("quan/", "quan_home.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
        return super(QuanView,self).get(request,*args,**kwargs)


class QuanCategoryView(TemplateView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name, self.category = get_default_template("quan/", "questions.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat")), QuestionsCategory.objects.get(name_en=self.kwargs["cat_name"])
		return super(QuanCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(QuanCategoryView,self).get_context_data(**kwargs)
		context["category"] = self.category
		context["quest_categories"] = QuestionsCategory.objects.only("pk")
		return context

	def get_queryset(self):
		questions = Question.objects.filter(category=self.category)
		return questions
