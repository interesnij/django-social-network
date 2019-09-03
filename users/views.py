from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin


class AllUsers(TemplateView,CategoryListMixin):
	template_name="all_users.html"
