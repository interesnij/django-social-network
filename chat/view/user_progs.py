""" TemplateView """
from django.views.generic import TemplateView
from django.views.generic import ListView


class CreateUserChat(TemplateView):
	""" если у инициатора нет друзей, показываем форму пустого чата. Если есть, то с возможностью добавлять друзей в чат.
	    Третий и четвертый варианты - пока не понятны, но зачем то я их задумал. Пока не ясно, что я хотел этим сказать
	"""
	template_name, member = None, None

	def get(self,request,*args,**kwargs):
		from common.templates import get_my_template
		from users.models import User

		self.user = User.objects.get(pk=self.kwargs["pk"])
		if self.user != request.user:
			self.member = self.user

		if self.user == request.user and not request.user.get_6_friends():
			self.template_name = get_my_template("chat/chat/create_chat_empty.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.user == request.user and request.user.get_6_friends():
			self.template_name = get_my_template("chat/chat/create_chat_with_members.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.user != request.user and not request.user.get_6_friends():
			self.template_name = get_my_template("chat/chat/create_chat_send_message.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.user != request.user and request.user.get_6_friends():
			self.template_name = get_my_template("chat/chat/create_chat_send_message_with_members.html", request.user, request.META['HTTP_USER_AGENT'])

		return super(CreateUserChat,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from chat.forms import ChatForm

		c = super(CreateUserChat,self).get_context_data(**kwargs)
		c["form"], c["member"] = ChatForm(), self.user
		return c

	def post(self,request,*args,**kwargs):
		from common.templates import render_for_platform
		from users.models import User
		from chat.models import ChatUsers
		from chat.forms import ChatForm

		self.form = ChatForm(request.POST)
		if self.form.is_valid() and request.is_ajax():
			new_chat = self.form.save(commit=False)
			new_chat.creator = request.user
			new_chat = self.form.save()
			ChatUsers.create_membership(user=request.user, is_administrator=True, chat=new_chat)
			favourite_messages_count = request.user.favourite_messages_count()
			get_header_chat = self.chat.get_header_chat(new_chat.pk)
			if request.POST.get('users'):
				new_chat.invite_users_in_chat(request.POST.getlist('users'), request.user)
			return render_for_platform(request, 'chat/chat/detail/chat.html', {, 'chat': new_chat, 'get_header_chat': get_header_chat, 'favourite_messages_count': favourite_messages_count})
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()


class UserSendPageMessage(TemplateView):
	""" Пишем сообщения со страниц пользователей или разных списков. Если у пользователя есть друзья,
	    то add_friend_message.html (возможность добавлять друзей), иначе add_message.html
	"""
	template_name = None

	def get(self,request,*args,**kwargs):
		from users.models import User
		from common.templates import get_settings_template

		if request.user.get_6_friends():
			self.template_name = get_settings_template("chat/message/add_friend_message.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_settings_template("chat/message/add_message.html", request.user, request.META['HTTP_USER_AGENT'])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		return super(UserSendPageMessage,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from chat.forms import MessageForm

		context = super(UserSendPageMessage,self).get_context_data(**kwargs)
		context["form"] = MessageForm()
		context["member"] = self.user
		return context

	def post(self,request,*args,**kwargs):
		from users.models import User
		from chat.models import Message
		from common.check.user import check_user_can_get_list
		from chat.forms import MessageForm
		from django.http import HttpResponse

		self.form, self.user, connections = MessageForm(request.POST), User.objects.get(pk=self.kwargs["pk"]), request.POST.getlist("chat_items")
		check_user_can_get_list(request.user, self.user)

		if request.is_ajax() and self.form.is_valid():
			message = self.form.save(commit=False)
			if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
				if connections:
					connections += [self.user.pk,]
					_message = Message.create_chat_append_members_and_send_message(creator=request.user, users_ids=connections, text=message.text, voice=request.POST.get('voice'), attach=request.POST.getlist('attach_items'), sticker=request.POST.get('sticker'))
				else:
					_message = Message.get_or_create_chat_and_send_message(creator=request.user, repost=None, user=self.user, text=message.text, voice=request.POST.get('voice'), attach=request.POST.getlist('attach_items'), sticker=request.POST.get('sticker'))
				return HttpResponse()
			else:
				from django.http import HttpResponseBadRequest
				return HttpResponseBadRequest()


class LoadUserChatMessage(TemplateView):
	""" Отрисовываем новое сообщение для всех участников чата, кроме текущего (это фильтруем в socket.js) - он его и так увидит сразу.
		Отрисовываем на странице чата.
	"""
	template_name = None
	def get(self,request,*args,**kwargs):
		from common.templates import get_my_template
		from chat.models import Message

		self.message, self.template_name = Message.objects.get(uuid=self.kwargs["uuid"]), get_my_template("chat/message/load_chat_message.html", request.user, request.META['HTTP_USER_AGENT'])
		self.message.unread = False
		self.message.save(update_fields=["unread"])
		return super(LoadUserChatMessage,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadUserChatMessage,self).get_context_data(**kwargs)
		context["object"] = self.message
		return context

class LoadUserMessage(TemplateView):
	""" Отрисовываем новое сообщение для всех участников чата, кроме текущего (это фильтруем в socket.js) - он его и так увидит сразу.
		Отрисовываем на странице всех чатов.
	"""
	template_name = None

	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from common.templates import get_my_template

		self.message = Message.objects.get(uuid=self.kwargs["uuid"])
		self.chat = self.message.chat
		self.template_name = get_my_template("chat/message/load_message.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadUserMessage,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadUserMessage,self).get_context_data(**kwargs)
		context["object"] = self.chat
		return context


""" View """
from django.views import View

class UserSendMessage(View):
	def post(self,request,*args,**kwargs):
		from common.templates import render_for_platform
		from chat.models import Message, Chat
		from chat.forms import MessageForm

		chat, form_post = Chat.objects.get(pk=self.kwargs["pk"]), MessageForm(request.POST, request.FILES)
		if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker') or request.POST.get('transfer') or request.POST.get('voice'):
			message = form_post.save(commit=False)

			new_message = Message.send_message(
											chat=chat,
											creator=request.user,
											repost=None,
											text=message.text,
											voice=message.voice,
											sticker=request.POST.get('sticker'),
											parent=request.POST.get('parent'),
											transfer=request.POST.getlist('transfer'),
											attach=request.POST.getlist('attach_items'))
			return render_for_platform(request, 'chat/message/message.html', {'object': new_message})
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()

class UserSendMessage(View):
	def post(self,request,*args,**kwargs):
		from chat.models import Message, Chat
		from chat.forms import MessageForm

		chat, form_post = Chat.objects.get(pk=self.kwargs["pk"]), MessageForm(request.POST, request.FILES)
		if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker') or request.POST.get('transfer') or request.POST.get('voice'):
			message = form_post.save(commit=False)

			new_message = Message.send_message(
											chat=chat,
											creator=request.user,
											repost=None,
											text=message.text,
											voice=message.voice,
											sticker=request.POST.get('sticker'),
											parent=request.POST.get('parent'),
											transfer=request.POST.getlist('transfer'),
											attach=request.POST.getlist('attach_items'))
			if new_message.voice:
				import json
				from django.http import HttpResponse
				return HttpResponse(json.dumps({"uuid": str(new_message.uuid)}),content_type="application/json")
			else:
				from common.templates import render_for_platform
				return render_for_platform(request, 'chat/message/message.html', {'object': new_message})
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()

class UserSaveDraftMessage(View):
	def post(self,request,*args,**kwargs):
		from chat.models import Message, Chat
		from chat.forms import MessageForm
		from django.http import HttpResponse

		chat, form_post = Chat.objects.get(pk=self.kwargs["pk"]), MessageForm(request.POST)
		message = form_post.save(commit=False)
		Message.save_draft_message(chat=chat,creator=request.user,text=message.text,parent=request.POST.get('parent'),attach=request.POST.getlist('attach_items'), transfer=request.POST.getlist('transfer'),)
		chat.read_messages(request.user.pk)
		return HttpResponse()

class UserMessageEdit(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_my_template
		from chat.models import Message

		self.message, self.template_name = Message.objects.get(uuid=self.kwargs["uuid"]), get_my_template("chat/message/edit_message.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserMessageEdit,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from chat.forms import MessageForm

		context = super(UserMessageEdit,self).get_context_data(**kwargs)
		context["object"] = self.message
		context["form"] = MessageForm(instance=self.message)
		return context

	def post(self, request, *args, **kwargs):
		from chat.models import Message
		from common.templates import render_for_platform

		_message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax():
			if request.POST.get('text') or request.POST.get('attach_items'):
				_message.edit_message(text=request.POST.get('text'), attach=request.POST.getlist('attach_items'))
			return render_for_platform(request, 'chat/message/new_edit_message.html', {'object': _message})
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()


class UserMessageFixed(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from django.http import Http404
		from common.templates import render_for_platform

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and message.chat.is_user_can_fix_item(request.user.pk):
			info_message = message.fixed_message_for_user_chat(request.user)
			return render_for_platform(request, 'chat/message/info_message.html', {'object': info_message})
		else:
			raise Http404

class UserMessageUnFixed(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from django.http import Http404, HttpResponse

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and message.chat.is_user_can_fix_item(request.user.pk):
			info_message = message.unfixed_message_for_user_chat(request.user)
			return HttpResponse()
		else:
			raise Http404


class UserMessagesFavorite(View):
	def get(self,request,*args,**kwargs):
		from django.http import HttpResponse, Http404
		from chat.models import Message

		if request.is_ajax():
			Message.add_favourite_messages(request.user.pk, request.GET.get("list"))
			return HttpResponse()
		else:
			raise Http404

class UserMessagesUnFavorite(View):
	def get(self,request,*args,**kwargs):
		from django.http import HttpResponse, Http404
		from chat.models import Message

		if request.is_ajax():
			Message.remove_favourite_messages(request.user.pk, request.GET.get("list"))
			return HttpResponse()
		else:
			raise Http404


class UserMessageDelete(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.pk in message.chat.get_members_ids():
			message.delete_item(request.user.pk, None)
			return HttpResponse()
		else:
			raise Http404

class UserMessageRecover(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and request.user.pk in message.chat.get_members_ids():
			message.restore_item(request.user.pk, None)
			return HttpResponse()
		else:
			raise Http404


class PhotoAttachInChatUserCreate(View):
	def post(self, request, *args, **kwargs):
		from gallery.models import Photo
		from common.templates import render_for_platform

		photos = []
		if request.is_ajax():
			for p in request.FILES.getlist('file'):
				photo = Photo.objects.create(creator=request.user, preview=p,file=p, type="_MES")
				photos += [photo,]
			return render_for_platform(request, 'chat/create/u_new_photos.html',{'object_list': photos})
		else:
			raise Http404


class UserChatMemberDelete(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from chat.models import Chat, ChatUsers
		from django.http import HttpResponse

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax() and chat.creator == request.user:
			chat.delete_member(user=user, creator=request.user)
			return HttpResponse()
		else:
			raise Http404

class ExitUserFromUserChat(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from chat.models import Chat
		from django.http import HttpResponse

		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and chat.creator == request.user:
			chat.exit_member(user=request.user)
			return HttpResponse()
		else:
			raise Http404


class UserChatAdminCreate(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from django.http import HttpResponse
		from chat.models import Chat

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax() and request.user.is_administrator_of_chat(chat.pk):
			new_admin = chat.add_administrator(user)
			return HttpResponse()
		else:
			raise Http404

class UserChatAdminDelete(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from django.http import HttpResponse
		from chat.models import Chat

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax() and request.user.is_administrator_of_chat(chat.pk):
			new_admin = chat.remove_administrator(user)
			return HttpResponse()
		else:
			raise Http404


class UserChatBeepOff(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Chat, ChatUsers
		from django.http import HttpResponse
		from datetime import datetime, timedelta

		chat = Chat.objects.get(pk=self.kwargs["pk"])
		chat_user = ChatUsers.objects.get(chat_id=chat.pk, user_id=request.user.pk)
		if request.is_ajax():
			chat_user.no_disturb = datetime.now() + timedelta(weeks=100)
			chat_user.save(update_fields=["no_disturb"])
			return HttpResponse()
		else:
			raise Http404


class UserChatBeepOn(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Chat, ChatUsers
		from django.http import HttpResponse

		chat = Chat.objects.get(pk=self.kwargs["pk"])
		chat_user = ChatUsers.objects.get(chat_id=chat.pk, user_id=request.user.pk)
		if request.is_ajax():
			chat_user.no_disturb = None
			chat_user.save(update_fields=["no_disturb"])
			return HttpResponse()
		else:
			raise Http404


class InviteMembersInUserChat(ListView):
	template_name, paginate_by, chat = None, 15, None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_settings_template

		self.template_name = get_settings_template("chat/chat/append_friends.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.GET.get("chat_pk") != "null":
			self.chat = Chat.objects.get(pk=request.GET.get("chat_pk"))
		return super(InviteMembersInUserChat,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(InviteMembersInUserChat,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		context["perm"] = self.request.user.profile_private
		return context

	def get_queryset(self):
		query = []

		r_user = self.request.user
		friends = r_user.get_all_friends()

		if self.chat:
			memders_ids = self.chat.get_recipients_ids(r_user.pk)
			for frend in friends:
				if frend.pk in memders_ids:
					pass
				else:
					if frend.is_user_can_add_in_chat(r_user.pk):
						query.append(frend)
		else:
			for frend in friends:
				if frend.is_user_can_add_in_chat(r_user.pk):
					query.append(frend)
		return query

	def post(self,request,*args,**kwargs):
		if request.is_ajax():
			from common.templates import render_for_platform
			from chat.models import Chat
			from django.http import HttpResponse

			if request.GET.get("chat_pk") != "null":
				self.chat = Chat.objects.get(pk=request.GET.get("chat_pk"))
				list = request.POST.getlist('users')
				info_messages = self.chat.invite_users_in_chat(list, request.user)
				return render_for_platform(request, 'chat/chat/new_manager_messages.html', {'object_list': info_messages})
			else:
				return HttpResponse()
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()


class UserChatDelete(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from django.http import HttpResponse, Http404

		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user/is_administrator_of_chat(chat.pk):
			chat.delete_chat()
			return HttpResponse()
		else:
			raise Http404

class UserChatRecover(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from django.http import HttpResponse, Http404

		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and request.user.is_administrator_of_chat(chat.pk):
			chat.restore_chat()
			return HttpResponse()
		else:
			raise Http404

class UserChatCleanMessages(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Chat, Message, MessageOptions
		from django.http import HttpResponse

		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated and request.user.pk in chat.get_members_ids():
			list = chat.get_messages_uuids(request.user.pk)
			objs = [
				MessageOptions(
						message_id = e,
						user_id = request.user.pk,
						is_deleted = True
					)
					for e in list
				]
			MessageOptions.objects.bulk_create(objs)
		return HttpResponse()


class UserChatEdit(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_detect_platform_template

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		if self.chat.is_user_can_see_settings(request.user.pk):
			self.template_name = get_detect_platform_template("chat/chat/info/settings.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserChatEdit,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserChatEdit,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		return context

	def post(self,request,*args,**kwargs):
		from chat.models import Chat
		from chat.forms import ChatForm
		from django.http import HttpResponse

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.form = ChatForm(request.POST, request.FILES, instance=self.chat)
		if request.is_ajax() and self.form.is_valid() and self.chat.is_user_can_see_settings(request.user.pk):
			chat = self.form.save(commit=False)
			chat.edit_chat(name=chat.name,description=chat.description,image=request.FILES.get('image'),)
			return HttpResponse()
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()
		return super(UserChatEdit,self).get(request,*args,**kwargs)


class UserChatPrivate(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_detect_platform_template

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])

		if self.chat.is_user_can_see_settings(request.user.pk):
			self.template_name = get_detect_platform_template("chat/chat/info/private.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserChatPrivate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserChatPrivate,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		return context

	def post(self,request,*args,**kwargs):
		from chat.models import Chat
		from django.http import HttpResponse

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and self.chat.is_user_can_see_settings(request.user.pk):
			self.type = request.GET.get("action")
			self.value = request.GET.get("value")
			if self.value == 6 or self.value == 5:
				return HttpResponse()

			if self.type == "can_add_members":
				self.chat.can_add_members = self.value
			elif self.type == "can_fix_item":
				self.chat.can_fix_item = self.value
			elif self.type == "can_add_admin":
				self.chat.can_add_admin = self.value
			elif self.type == "can_mention":
				self.chat.can_mention = self.value
			elif self.type == "can_add_design":
				self.chat.can_add_design = self.value
			elif self.type == "can_see_settings":
				self.chat.can_see_settings = self.value
			elif self.type == "can_see_log":
				self.chat.can_see_log = self.value
			self.chat.save()
			return HttpResponse()
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()
		return super(UserChatPrivate,self).get(request,*args,**kwargs)

class UserChatIncludeUsers(ListView):
	template_name, users = None, []

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_detect_platform_template

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.type = request.GET.get("action")
		if self.type == "can_add_members":
			self.users = self.chat.get_add_in_chat_include_users()
			self.text = "приглашать участников в чат"
		elif self.type == "can_fix_item":
			self.users = self.chat.get_can_fix_item_include_users()
			self.text = "закреплять сообщения в чате"
		elif self.type == "can_add_admin":
			self.users = self.chat.get_can_add_admin_include_users()
			self.text = "Добавлять/удалять админов чата"
		elif self.type == "can_mention":
			self.users = self.chat.get_can_mention_include_users()
			self.text = "Упоминать чат в соцсети"
		elif self.type == "can_add_design":
			self.users = self.chat.get_can_add_design_include_users()
			self.text = "Менять дизайн чата"
		elif self.type == "can_see_settings":
			self.users = self.chat.get_can_see_settings_include_users()
			self.text = "видеть настройки чата"
		elif self.type == "can_see_log":
			self.users = self.chat.get_can_see_log_include_users()
			self.text = "видеть журнал действий"
		if self.chat.is_user_can_see_settings(request.user.pk):
			self.template_name = get_detect_platform_template("chat/chat/info/include_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserChatIncludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserChatIncludeUsers,self).get_context_data(**kwargs)
		context["users"] = self.users
		context["chat"] = self.chat
		context["text"] = self.text
		context["type"] = self.type
		return context

	def get_queryset(self):
		return self.chat.get_members()

	def post(self,request,*args,**kwargs):
		from chat.models import Chat
		from django.http import HttpResponse

		if request.is_ajax():
			self.chat = Chat.objects.get(pk=self.kwargs["pk"])
			self.chat.post_include_users(request.POST.getlist("users"), request.POST.get("type"))
		return HttpResponse()

class UserChatExcludeUsers(ListView):
	template_name, users = None, []

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_detect_platform_template

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.type = request.GET.get("action")
		if self.type == "can_add_members":
			self.users = self.chat.get_add_in_chat_exclude_users()
			self.text = "приглашать участников в чат"
		elif self.type == "can_fix_item":
			self.users = self.chat.get_can_fix_item_exclude_users()
			self.text = "закреплять сообщения в чате"
		elif self.type == "can_add_admin":
			self.users = self.chat.get_can_add_admin_exclude_users()
			self.text = "добавлять/удалять админов чата"
		elif self.type == "can_mention":
			self.users = self.chat.get_can_mention_exclude_users()
			self.text = "Упоминать чат в соцсети"
		elif self.type == "can_add_design":
			self.users = self.chat.get_can_add_design_exclude_users()
			self.text = "Менять дизайн чата"
		elif self.type == "can_see_settings":
			self.users = self.chat.get_can_see_settings_exclude_users()
			self.text = "видеть настройки чата"
		elif self.type == "can_see_log":
			self.users = self.chat.get_can_see_log_exclude_users()
			self.text = "видеть журнал действий"
		if self.chat.is_user_can_see_settings(request.user.pk):
			self.template_name = get_detect_platform_template("chat/chat/info/exclude_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserChatExcludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserChatExcludeUsers,self).get_context_data(**kwargs)
		context["users"] = self.users
		context["chat"] = self.chat
		context["text"] = self.text
		context["type"] = self.type
		return context

	def get_queryset(self):
		return self.chat.get_members()

	def post(self,request,*args,**kwargs):
		from chat.models import Chat
		from django.http import HttpResponse

		if request.is_ajax():
			self.chat = Chat.objects.get(pk=self.kwargs["pk"])
			self.chat.post_exclude_users(request.POST.getlist("users"), request.POST.get("type"))
			return HttpResponse('ok')
		return HttpResponse('not ok')
