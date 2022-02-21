from django.views.generic.base import TemplateView
from django.views.generic import ListView
from quan.models import Question, QuestionsCategory
from common.templates import get_default_template


class QuanView(TemplateView):
    template_name, i_support = None, None

    def get(self,request,*args,**kwargs):
        self.template_name = get_default_template("quan/", "quan_home.html", request.user, request.META['HTTP_USER_AGENT'])
        if request.user.is_autenticated:
            from managers.models import SupportUsers
            if request.user.is_superuser or SupportUsers.objects.filter(manager=request.user.pk).exists():
                self.i_support = True
        return super(QuanView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(QuanView,self).get_context_data(**kwargs)
        context["i_support"] = self.i_support
        return context


class QuanCategoryView(TemplateView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name, self.category = get_default_template("quan/", "questions.html", request.user, request.META['HTTP_USER_AGENT']), QuestionsCategory.objects.get(name_en=self.kwargs["cat_name"])
		return super(QuanCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(QuanCategoryView,self).get_context_data(**kwargs)
		context["category"] = self.category
		context["quest_categories"] = QuestionsCategory.objects.only("pk")
		return context

	def get_queryset(self):
		questions = Question.objects.filter(category=self.category)
		return questions
