from django.views.generic.base import ContextMixin
from django.conf import settings
from main.models import EmojiGroup, Emoji



class CategoryListMixin(ContextMixin):
	emojies_1 = Emoji.objects.filter(group=1)
	def get_context_data(self,**kwargs):
		context=super(CategoryListMixin,self).get_context_data(**kwargs)
		context["current_url"]=self.request.path
		context["emojies_1"]=self.emojies_1
		return context

class PageNumberMixin(CategoryListMixin):
	def get_context_data(self,**kwargs):
		context=super(PageNumberMixin,self).get_context_data(**kwargs)
		try:
			context["pn"]=self.request.GET["page"]
		except KeyError:
			context["pn"]="1"
		return context
