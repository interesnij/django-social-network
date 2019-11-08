from django.views.generic.base import ContextMixin
from django.conf import settings
from common.models import EmojiGroup, Emoji



class EmojiListMixin(ContextMixin):
	emojies_1 = Emoji.objects.filter(group=1)
	emojies_2 = Emoji.objects.filter(group=2)
	def get_context_data(self,**kwargs):
		context=super(EmojiListMixin,self).get_context_data(**kwargs)
		context["current_url"]=self.request.path
		context["emojies_1"]=self.emojies_1
		context["emojies_2"]=self.emojies_2
		return context
