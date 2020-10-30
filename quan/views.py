from django.views.generic import ListView
from quan.models import Question, QuestionsCategory
from common.template.user import get_detect_platform_template 


class QuanCategoryView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_platform_template("quan/questions.html", request.META['HTTP_USER_AGENT'])
		self.category = QuestionsCategory.objects.get(name_en=self.kwargs["cat_name"])
		return super(QuanCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(QuanCategoryView,self).get_context_data(**kwargs)
		context["category"] = self.category
		context["quest_categories"] = QuestionsCategory.objects.only("pk")
		return context

	def get_queryset(self):
		questions = Question.objects.filter(category=self.category)
		return questions
