from django.views.generic.base import ContextMixin
from django.conf import settings
from posts.forms import PostForm


class FormMixin(ContextMixin):
	def get_context_data(self,**kwargs):
		context=super(FormMixin,self).get_context_data(**kwargs)
		context["form_post"]=PostForm()
		return context
