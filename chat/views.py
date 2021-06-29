""" ListView """
from django.views.generic import ListView

class MessagesListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.template.user import get_settings_template

		self.template_name, self.user = get_settings_template("chat/chat/list.html", request.user, request.META['HTTP_USER_AGENT']), request.user
		return super(MessagesListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MessagesListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		chats = self.user.get_all_chats()
		return chats


class ChatDetailView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.template.user import get_settings_template

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		if self.chat.is_private():
			self.template_name = get_settings_template("chat/chat/detail/private_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.chat.is_group():
			self.template_name = get_settings_template("chat/chat/detail/group_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.chat.is_manager():
			self.template_name = get_settings_template("chat/chat/detail/manager_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		unread_messages = self.chat.get_unread_message(request.user.pk)
		unread_messages.update(unread=False)
		self.get_messages = self.chat.get_messages_for_recipient(request.user.pk)
		self.get_fix_message = self.chat.get_fix_message_for_recipient(request.user.pk)
		return super(ChatDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatDetailView,self).get_context_data(**kwargs)
		context['chat'] = self.chat
		context['object'] = self.get_fix_message
		return context

	def get_queryset(self):
		return self.get_messages
