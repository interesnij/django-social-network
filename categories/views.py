from django.views.generic.base import TemplateView
from .models import Category


class CategoriesView(TemplateView):
    template_name="categories.html"
