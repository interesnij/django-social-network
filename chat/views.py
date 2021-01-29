""" ListView """
from django.views.generic import ListView

class MessagesListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.template.user import get_settings_template

		self.user, self.template_name = get_settings_template("chat/chat/list.html", request.user, request.META['HTTP_USER_AGENT']), request.user
		return super(MessagesListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MessagesListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		return self.user.get_all_chats()


class ChatDetailView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.template.user import get_settings_template

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		if self.chat.is_private():
			self.template_name = get_settings_template("chat/chat/private_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.chat.is_public():
			self.template_name = get_settings_template("chat/chat/public_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.chat.is_manager():
			self.template_name = get_settings_template("chat/chat/manager_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		self.pk = request.user.pk
		unread_messages = self.chat.get_unread_message(self.pk)
		unread_messages.update(unread=False)
		return super(ChatDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatDetailView,self).get_context_data(**kwargs)
		context['chat'] = self.chat
		return context

	def get_queryset(self):
		return self.chat.get_messages().order_by("-created")
