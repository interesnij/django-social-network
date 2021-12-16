""" ListView """
from django.views.generic import ListView


class ChatsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_settings_template

		self.template_name, self.user = get_settings_template("chat/chat/list.html", request.user, request.META['HTTP_USER_AGENT']), request.user
		self.favourite_messages_count = request.user.favourite_messages_count()
		return super(ChatsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatsListView,self).get_context_data(**kwargs)
		context['favourite_messages_count'] = self.favourite_messages_count
		return context

	def get_queryset(self):
		chats = self.user.get_all_chats()
		return chats


class ChatDetailView(ListView):
	template_name, paginate_by, can_add_members_in_chat, favourite_messages, favourite_messages_count = None, 15, None, None, None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_settings_template
		from asgiref.sync import async_to_sync
		from channels.layers import get_channel_layer

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("chat/chat/detail/chat.html", request.user, request.META['HTTP_USER_AGENT'])

		self.pk = request.user.pk
		self.messages = self.chat.get_messages(self.pk)
		unread_messages = self.chat.get_unread_message(self.pk)
		unread_messages.update(unread=False)
		self.favourite_messages_count = request.user.favourite_messages_count()
		self.get_header_chat = self.chat.get_header_chat(self.pk)

		channel_layer = get_channel_layer()
		payload = {
			'type': 'receive',
			'key': 'message',
			'chat_id': self.chat.pk,
			'recipient_ids': str(self.chat.get_recipients_ids(self.pk)),
			'name': "u_message_read",
		}
		async_to_sync(channel_layer.group_send)('notification', payload)
		return super(ChatDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatDetailView,self).get_context_data(**kwargs)
		context['chat'] = self.chat
		context['fix_message'] = self.chat.get_first_fix_message
		context['get_header_chat'] = self.get_header_chat
		context['can_add_members'] = self.can_add_members_in_chat
		if self.chat.is_have_draft_message(self.pk):
			context['get_message_draft'] = self.chat.get_draft_message(self.pk)

		context['favourite_messages_count'] = self.favourite_messages_count
		return context

	def get_queryset(self):
		return self.messages


class ChatFixedMessagesView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_settings_template
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


class ChatInfo(ListView):
	template_name, paginate_by = None, 20

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_chat
		from chat.models import Chat

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_template_user_chat(self.chat, "chat/chat/info/", "info.html", request.user, request.META['HTTP_USER_AGENT'])
		self.is_can_see_settings = self.chat.is_user_can_edit_info(request.user.pk)
		self.is_can_add_admin = self.chat.is_user_can_add_admin(request.user.pk)
		self.is_user_can_add_members = self.chat.is_user_can_add_members(request.user.pk)
		return super(ChatInfo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatInfo,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		context["is_can_see_settings"] = self.is_can_see_settings
		context["is_user_can_add_admin"] = self.is_can_add_admin
		context["is_user_can_add_members"] = self.is_user_can_add_members
		return context

	def get_queryset(self):
		return self.chat.get_members()
