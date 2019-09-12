from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from users.models import User


class MainPageView(TemplateView,CategoryListMixin):
	if request.user:
		template_name="main/mainpage.html"
	else:
		template_name="main/auth.html"

	def get(self,request,*args,**kwargs):
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(MainPageView,self).get_context_data(**kwargs)

		return context
