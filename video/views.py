from django.views.generic.base import TemplateView
from users.models import User


class AllVideoView(TemplateView):
    template_name="all_video.html"
