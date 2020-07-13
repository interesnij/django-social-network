from django.views.generic import TemplateView
from goods.models import GoodSubCategory


class GoodCategories(TemplateView):
	template_name = "good_base/categories.html"


class GoodSubCategories(TemplateView):
	template_name = "good_base/subcategories.html"


class GoodsCats(TemplateView):
	template_name = "good_base/cats.html"
	categ = None

	def get(self,request,*args,**kwargs):
		self.categ = GoodSubCategory.objects.filter(category__order=self.kwargs["order"])
		return super(GoodsCats,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GoodsCats,self).get_context_data(**kwargs)
		context["categ"] = self.categ
		return context
