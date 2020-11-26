import json
from users.models import User
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.utils.safestring import mark_safe
from chat.models import Message, Chat
from common.template.user import get_settings_template


class MessagesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		self.template_name = get_settings_template("chat/chat/list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MessagesListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MessagesListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		list = self.user.get_all_chats()
		return list


class ChatDetailView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
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
		self.chat_members = self.chat.chat_relation.exclude(user_id=self.pk)[:3]
		self.list = self.chat.get_messages()
		return super(ChatDetailView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatDetailView,self).get_context_data(**kwargs)
		context['chat'] = self.chat
		context['chat_members'] = self.chat_members
		return context

	def get_queryset(self):
		list = self.list
		return list
