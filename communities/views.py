from django.views.generic.base import TemplateView
from communities.models import Community


class CommunitiesView(TemplateView):
    template_name="communities.html"
