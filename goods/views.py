from django.shortcuts import render
from django.views.generic import TemplateView


class GoodCategoriesView(TemplateView):
	template_name="good_categories.html"

class GoodSubCategoriesView(TemplateView):
	template_name="good_subcategories.html"

class GoodsView(TemplateView):
	template_name="goods.html"
