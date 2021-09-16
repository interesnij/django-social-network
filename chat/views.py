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
		from asgiref.sync import async_to_sync
		from channels.layers import get_channel_layer

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.pk = request.user.pk
		if self.chat.is_private():
			self.template_name = get_settings_template("chat/chat/detail/private_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.chat.is_group():
			self.template_name = get_settings_template("chat/chat/detail/group_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.chat.is_manager():
			self.template_name = get_settings_template("chat/chat/detail/manager_chat.html", request.user, request.META['HTTP_USER_AGENT'])
		unread_messages = self.chat.get_unread_message(self.pk)
		unread_messages.update(unread=False)
		self.get_messages = self.chat.get_messages_for_recipient(self.pk)

		channel_layer = get_channel_layer()
		payload = {
			'type': 'receive',
			'key': 'message',
			'chat_id': self.chat.pk,
			'recipient_ids': str(self.chat.get_recipients_ids(request.user.pk)),
			'name': "u_message_read",
		}
		async_to_sync(channel_layer.group_send)('notification', payload)
		return super(ChatDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatDetailView,self).get_context_data(**kwargs)
		context['chat'] = self.chat
		context['fix_message'] = self.chat.get_first_fix_message
		if self.chat.is_have_draft_message(self.pk):
			context['get_message_draft'] = self.chat.get_draft_message(self.pk)
		return context

	def get_queryset(self):
		return self.get_messages


class ChatFixedMessagesView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.template.user import get_settings_template
		from chat.models import Chat

		self.template_name, self.chat = get_settings_template("chat/chat/fixed_list.html", request.user, request.META['HTTP_USER_AGENT']), Chat.objects.get(pk=self.kwargs["pk"])
		return super(ChatFixedMessagesView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatFixedMessagesView,self).get_context_data(**kwargs)
		context['chat'] = self.chat
		return context

	def get_queryset(self):
		chats = self.chat.get_fixed_messages()
		return chats
