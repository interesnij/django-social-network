from django.views.generic import ListView
from quan.models import Question, QuestionsCategory


class QuanCategoryView(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
        self.category = QuestionsCategory.objects.get(name_en=self.kwargs["cat_name"])
		self.template_name = "questions.html"
		return super(QuanCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(QuanCategoryView,self).get_context_data(**kwargs)
		context["category"] = self.category
		context["quest_categories"] = QuestionsCategory.objects.only("pk")
		return context

	def get_queryset(self):
		questions = Question.objects.filter(category=self.category)
		return questions
