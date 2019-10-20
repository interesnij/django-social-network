from django.shortcuts import render
from django.views.generic import TemplateView
from goods.models import Good
from django.views.generic import ListView
from users.models import User
from django.http import HttpResponse


class GoodCategoriesView(TemplateView):
	template_name="good_categories.html"


class GoodSubCategoriesView(TemplateView):
	template_name="good_subcategories.html"


class GoodsListView(ListView):
	template_name="goods.html"
	model=Good

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.goods=Good.objects.filter(user=self.user)
		return super(GoodsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GoodsListView,self).get_context_data(**kwargs)
		context["user"]=self.user
		context['goods'] = self.goods
		return context
