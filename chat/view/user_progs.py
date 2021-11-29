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
			new_chat.type = "GRO"
			new_chat.save(update_fields=["type"])
			ChatUsers.create_membership(user=request.user, is_administrator=True, chat=new_chat)
			members = [request.user, ]

			connections = request.POST.getlist("connections")
			for user_id in connections:
				user = User.objects.get(pk=user_id)
				ChatUsers.create_membership(user=user, chat=new_chat)
				members += [user, ]

			if new_chat.is_private():
				template = 'chat/chat/detail/private_chat.html'
			elif new_chat.is_group():
				template = 'chat/chat/detail/group_chat.html'
			return render_for_platform(request, template, {'chat': new_chat, 'chat_members': members, 'user': request.user})
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
		Отрисовываем на странице чата.
	"""
	template_name = None

	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from common.templates import get_my_template

		self.message = Message.objects.get(uuid=self.kwargs["uuid"])
		self.chat = self.message.chat
		first_message, creator_figure, user_id, self.template_name = self.chat.get_first_message(request.user.pk), '', request.user.pk, get_my_template("chat/message/load_message.html", request.user, request.META['HTTP_USER_AGENT'])
		if self.chat.is_private():
			member = self.chat.get_chat_member(user_id)
			if self.chat.image:
				figure = '<figure><img src="' + self.chat.image.url + '" style="border-radius:50px;width:50px;" alt="image"></figure>'
			elif member.get_avatar():
				figure = '<figure><img src="' + member.get_avatar() + '" style="border-radius:50px;width:50px;" alt="image"></figure>'
			else:
				figure = '<figure><svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
			if self.chat.name:
				chat_name = self.chat.name
			else:
				chat_name = member.get_full_name()
			if member.get_online():
				status = ' <span class="status bg-success"></span>'
			else:
				status = ''
			if first_message.creator.id == user_id:
				creator_figure = '<span class="underline">Вы:</span> '
			media_body = '<div class="media-body"><h5 class="time-title mb-0">{}{}<small class="float-right text-muted">{}</small></h5><p class="mb-0" style="white-space: nowrap;">{}{}</p></div>'.format(chat_name, status, first_message.get_created(),creator_figure,first_message.get_preview_text())
			self.block = '<div class="media">{}{}{}</div>'.format(figure, media_body, self.chat.get_unread_count_message(user_id))
		elif self.chat.is_group():
			if self.chat.image:
				figure = '<figure><img src="' + self.chat.image.url + '"style="border-radius:50px;width:50px;" alt="image"></figure>'
			else:
				figure = '<figure><img src="/static/images/group_chat.jpg" style="border-radius:50px;width:50px;" alt="image"></figure>'
			if self.chat.name:
				chat_name = self.chat.name
			else:
				chat_name = "Групповой чат"
			if first_message.creator.id == user_id:
				creator_figure = '<span class="underline">Вы:</span> '
			media_body = '<div class="media-body"><h5 class="time-title mb-0">' + chat_name + '<small class="float-right text-muted">' + first_message.get_created() + '</small></h5><p class="mb-0" style="white-space: nowrap;">' + creator_figure + first_message.get_preview_text() + '</p></div>'
			self.block = '<div class="media">' + figure + media_body + self.chat.get_unread_count_message(user_id) + '</div>'
		return super(LoadUserMessage,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadUserMessage,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		context["block"] = str(self.block)
		return context


""" View """
from django.views import View

class UserSendMessage(View):
	def post(self,request,*args,**kwargs):
		from common.templates import render_for_platform
		from chat.models import Message, Chat
		from chat.forms import MessageForm

		chat, form_post = Chat.objects.get(pk=self.kwargs["pk"]), MessageForm(request.POST)
		if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker') or request.POST.get('transfer'):
			message = form_post.save(commit=False)
			new_message = Message.send_message(
											chat=chat,
											creator=request.user,
											repost=None,
											text=message.text,
											voice=request.POST.get('voice'),
											sticker=request.POST.get('sticker'),
											parent=request.POST.get('parent'),
											transfer=request.POST.getlist('transfer'),
											attach=request.POST.getlist('attach_items'))
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
		from common.check.message import check_can_send_message
		from chat.models import Message
		from django.http import Http404
		from common.templates import render_for_platform

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		check_can_send_message(request.user, message.chat)
		if request.is_ajax():
			info_message = message.fixed_message_for_user_chat(request.user)
			return render_for_platform(request, 'chat/message/info_message.html', {'object': info_message})
		else:
			raise Http404

class UserMessageUnFixed(View):
	def get(self,request,*args,**kwargs):
		from common.check.message import check_can_send_message
		from chat.models import Message
		from django.http import Http404
		from common.templates import render_for_platform

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax():
			check_can_send_message(request.user, message.chat)
			info_message = message.unfixed_message_for_user_chat(request.user)
			return render_for_platform(request, 'chat/message/message.html', {'object': info_message})
		else:
			raise Http404


class UserMessageFavorite(View):
	def get(self,request,*args,**kwargs):
		from common.check.message import check_can_send_message
		from chat.models import MessageFavorite, Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and not MessageFavorite.objects.filter(user_id=request.user.pk, message=message).exists():
			check_can_send_message(request.user, message.chat)
			MessageFavorite.objects.create(user=request.user, message=message)
			return HttpResponse()
		else:
			raise Http404

class UserMessageUnFavorite(View):
	def get(self,request,*args,**kwargs):
		from chat.models import MessageFavorite, Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and MessageFavorite.objects.filter(user_id=request.user.pk, message=message).exists():
			MessageFavorite.objects.get(user=request.user, message=message).delete()
			return HttpResponse()
		else:
			raise Http404


class UserMessageDelete(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and (request.user.pk == message.creator.pk or request.user.pk == message.recipient.pk):
			message.delete_item(None)
			return HttpResponse()
		else:
			raise Http404

class UserMessageRecover(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and (request.user.pk == message.creator.pk or request.user.pk == message.recipient.pk):
			message.restore_item(None)
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
		from chat.models import ChatUsers
		from django.http import HttpResponse

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax() and chat.creator == request.user:
			ChatUsers.delete_membership(user=user, chat=chat)
			return HttpResponse()
		else:
			raise Http404

class ExitUserFromUserChat(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from chat.models import ChatUsers
		from django.http import HttpResponse

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax() and chat.creator == request.user:
			ChatUsers.exit_membership(user=user, chat=chat)
			return HttpResponse()
		else:
			raise Http404

class AppendUserInUserChat(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from chat.models import ChatUsers
		from django.http import HttpResponse

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax() and chat.creator == request.user:
			ChatUsers.create_membership(user=user, chat=chat)
			return HttpResponse()
		else:
			raise Http404


class UserChatAdminCreate(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from django.http import HttpResponse

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
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_settings_template

		self.template_name = get_settings_template("chat/chat/append_friends.html", request.user, request.META['HTTP_USER_AGENT'])
		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		return super(InviteMembersInUserChat,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(InviteMembersInUserChat,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		context["perm"] = self.request.user.user_private
		return context

	def get_queryset(self):
		query = []

		r_user = self.request.user
		memders_ids = self.chat.get_recipients_ids(r_user.pk)
		friends = r_user.get_all_connection()
		for frend in friends:
			if frend.pk in memders_ids:
				pass
			else:
				if frend.is_user_can_add_in_chat(r_user.pk):
					query.append(frend)
		return query

	def post(self,request,*args,**kwargs):
		if request.is_ajax():
			from common.templates import render_for_platform
			from chat.models import Chat

			list = request.POST.getlist('chat_users')
			self.chat = Chat.objects.get(pk=self.kwargs["pk"])
			info_messages = self.chat.invite_users_in_chat(list, request.user)
			return render_for_platform(request, 'chat/chat/new_manager_messages.html', {'object_list': info_messages})
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


class UserChatEdit(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_template_admin_chat

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_template_admin_chat("chat/chat/info/settings.html", request.user, request.META['HTTP_USER_AGENT'])
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
		self.form = ChatForm(request.POST,instance=self.chat)
		if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_chat(self.chat.pk):
			chat = self.form.save(commit=False)
			chat.edit_chat(
				name=chat.name,
				description=chat.description,
				image=chat.image,
				can_add_members=chat.can_add_members,
				can_edit_info=chat.can_edit_info,
				can_fix_item=chat.can_fix_item,
				can_mention=chat.can_mention,
				can_add_admin=chat.can_add_admin,
				can_add_design=chat.can_add_design,)
			return HttpResponse()
		else:
			return HttpResponseBadRequest()
		return super(UserChatEdit,self).get(request,*args,**kwargs)
