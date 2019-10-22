from django.shortcuts import render
from django.views.generic import TemplateView
from goods.models import Good, GoodSubCategory, GoodCategory
from django.views.generic import ListView
from users.models import User
from django.http import HttpResponse, JsonResponse
from goods.forms import GoodForm
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from generic.mixins import CategoryListMixin


class GoodCategoriesView(TemplateView):
	template_name="good_categories.html"


class GoodSubCategoriesView(TemplateView):
	template_name="good_subcategories.html"


class GoodsListView(ListView):
	template_name="goods.html"
	model=Good

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.goods=Good.objects.filter(creator=self.user)
		return super(GoodsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GoodsListView,self).get_context_data(**kwargs)
		context["user"]=self.user
		context['goods'] = self.goods
		return context


class GoodUserCreate(TemplateView):
	template_name="good_add.html"
	form=None
	sub_categories = GoodSubCategory.objects.only("id")
	categories = GoodCategory.objects.only("id")
	success_url="/"

	def get(self,request,*args,**kwargs):
		self.form=GoodForm(initial={"creator":request.user})
		return super(GoodUserCreate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GoodUserCreate,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["sub_categories"]=self.sub_categories
		context["categories"]=self.categories
		return context

	def post(self,request,*args,**kwargs):
		self.form=GoodForm(request.POST,request.FILES)

		if self.form.is_valid():
			new_good=self.form.save(commit=False)
			new_good.creator=self.request.user
			new_good=self.form.save()

			if request.is_ajax() :
				html = render_to_string('goods.html',{'object': new_good,'request': request})
			return HttpResponse(html)
		else:
			return JsonResponse({'error': True, 'errors': self.form.errors})
		return super(GoodUserCreate,self).get(request,*args,**kwargs)


class GoodsCatsView(TemplateView):
	template_name="good_cats.html"
	categ = None

	def get(self,request,*args,**kwargs):

		self.categ = GoodSubCategory.objects.filter(category__order=self.kwargs["order"])
		return super(GoodsCatsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GoodsCatsView,self).get_context_data(**kwargs)
		context["categ"]=self.categ
		return context


class GoodDetailView(CategoryListMixin, TemplateView):
	template_name="good_detail.html"

	def get(self,request,*args,**kwargs):
		self.good = Good.objects.get(pk=self.kwargs["pk"])
		self.good.views += 1
		self.good.save()
		return super(GoodDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context=super(GoodDetailView,self).get_context_data(**kwargs)
		context["object"]=self.good
		return context
