from django.views.generic.base import TemplateView


class NotificationsView(TemplateView):
    template_name="notification.html"
