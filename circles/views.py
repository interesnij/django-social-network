from django.views.generic.base import TemplateView
from .models import Category


class CircleView(TemplateView):
    template_name="circles.html"
