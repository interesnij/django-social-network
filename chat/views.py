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
		return self.user.get_all_chats()


class ChatDetailView(ListView):
	template_name, paginate_by, can_add_members_in_chat, favourite_messages, favourite_messages_count = None, 15, None, None, None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_settings_template
		from asgiref.sync import async_to_sync
		from channels.layers import get_channel_layer

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.pk = request.user.pk
		if self.pk in self.chat.get_members_ids():
			self.template_name = get_settings_template("chat/chat/detail/chat.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404

		self.messages = self.chat.get_messages(self.pk)
		self.chat.read_messages(self.pk)
		self.favourite_messages_count = request.user.favourite_messages_count()
		self.get_header_chat = self.chat.get_header_chat(self.pk)
		self.is_admin = request.user.is_administrator_of_chat(self.chat.pk)

		channel_layer = get_channel_layer()
		payload = {
			'type': 'receive',
			'key': 'message',
			'chat_id': self.chat.pk,
			'recipient_id': str(request.user.pk),
			'name': "u_message_read",
		}
		async_to_sync(channel_layer.group_send)('notification', payload)
		return super(ChatDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatDetailView,self).get_context_data(**kwargs)
		context['chat'] = self.chat
		context['fix_message'] = self.chat.get_first_fix_message()
		context['get_header_chat'] = self.get_header_chat
		context['can_add_members'] = self.can_add_members_in_chat
		if self.chat.is_have_draft_message(self.pk):
			context['get_message_draft'] = self.chat.get_draft_message(self.pk)

		context['favourite_messages_count'] = self.favourite_messages_count
		context['is_admin'] = self.is_admin
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
		context['is_user_can_fix_item'] = self.chat.is_user_can_fix_item(self.request.user.pk)
		return context

	def get_queryset(self):
		return self.chat.get_fixed_messages()


class ChatInfo(ListView):
	template_name, paginate_by = None, 20

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_chat
		from chat.models import Chat

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		request_user_pk = request.user.pk
		self.template_name = get_template_user_chat(self.chat, "chat/chat/info/", "info.html", request.user, request.META['HTTP_USER_AGENT'])
		self.is_can_see_settings = self.chat.is_user_can_see_settings(request_user_pk)
		self.is_can_add_admin = self.chat.is_user_can_add_admin(request_user_pk)
		self.is_user_can_add_members = self.chat.is_user_can_add_members(request_user_pk)
		self.is_can_see_log = self.chat.is_user_can_see_log(request_user_pk)
		return super(ChatInfo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatInfo,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		context["is_can_see_settings"] = self.is_can_see_settings
		context["is_user_can_add_admin"] = self.is_can_add_admin
		context["is_user_can_add_members"] = self.is_user_can_add_members
		context["is_can_see_log"] = self.is_can_see_log
		return context

	def get_queryset(self):
		return self.chat.get_members()

class ChatCollections(ListView):
	template_name, paginate_by = None, 20

	def get(self,request,*args,**kwargs):
		from common.templates import get_settings_template
		from chat.models import Chat

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		type = request.GET.get("type")
		if not type:
			type, self.list = "photo", self.chat.get_attach_photos()
		elif type == "photo":
			self.list = self.chat.get_attach_photos()
		elif type == "doc":
			self.list = self.chat.get_attach_docs()
		elif type == "music":
			self.list = self.chat.get_attach_tracks()
		elif type == "video":
			self.list = self.chat.get_attach_videos()
		elif type == "good":
			self.list = self.chat.get_attach_goods()
		elif type == "post":
			self.list = self.chat.get_attach_posts()

		if request.user.pk in self.chat.get_members_ids():
			self.template_name = get_settings_template("chat/chat/collections/" + type + ".html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from django.http import Http404
			raise Http404
		return super(ChatCollections,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatCollections,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		return context

	def get_queryset(self):
		return self.list


class ChatFavouritesMessagesView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_settings_template

		self.template_name = get_settings_template("chat/chat/favourites_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(ChatFavouritesMessagesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.request.user.get_favourite_messages()

class ChatSearchView(ListView):
	template_name, paginate_by = None, 20

	def get(self,request,*args,**kwargs):
		from chat.models import Chat, Message
		from django.http import Http404
		from common.templates import get_detect_platform_template
		from django.db.models import Q

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		if not self.chat.is_public() and not request.user.pk in self.chat.get_members_ids():
			raise Http404
		elif request.GET.get('q'):
			_q = request.GET.get('q').replace("#", "%23")
			if "?stat" in _q:
				self.q = _q[:_q.find("?"):]
			else:
				self.q = _q
			query = Q(chat_id=self.chat)
			query.add(~Q(type__contains="_"), Q.AND)
			query.add(~Q(message_options__user_id=request.user.pk, message_options__is_deleted=True), Q.AND)
			query.add(Q(text__icontains=self.q), Q.AND)
			self.list = Message.objects.filter(query)
		else:
			self.q = ""
			self.list = []
		self.template_name = get_detect_platform_template("chat/chat/detail/search.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(ChatSearchView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(ChatSearchView,self).get_context_data(**kwargs)
		context["q"] = self.q.replace("%23","#")
		context["chat"] = self.chat
		return context

	def get_queryset(self):
		return self.list
