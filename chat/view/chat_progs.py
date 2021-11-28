

""" View """
from django.views import View

class ChatDelete(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from django.http import HttpResponse, Http404
		from common.check.message import check_can_change_chat

		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			check_can_change_chat(request.user, chat)
			chat.delete_chat()
			return HttpResponse()
		else:
			raise Http404

class ChatRecover(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from django.http import HttpResponse, Http404
		from common.check.message import check_can_change_chat

		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			check_can_change_chat(request.user, chat)
			chat.restore_chat()
			return HttpResponse()
		else:
			raise Http404
