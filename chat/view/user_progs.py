""" TemplateView """
from django.views.generic import TemplateView


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
		from common.template.user import render_for_platform
		from users.models import User
		from chat.models import ChatUsers
		from chat.forms import ChatForm

		self.form = ChatForm(request.POST)
		if self.form.is_valid() and request.is_ajax():
			new_chat = self.form.save(commit=False)
			new_chat.creator = request.user
			self.form.save()
			ChatUsers.create_membership(user=request.user, is_administrator=True, chat=new_chat)
			members = [request.user, ]

			connections = request.POST.getlist("connections")
			for user_id in connections:
				user = User.objects.get(pk=user_id)
				ChatUsers.create_membership(user=user, chat=new_chat)
				members += [user, ]

			if new_chat.is_private():
				template = 'chat/chat/private_chat.html'
			elif new_chat.is_public():
				template = 'chat/chat/public_chat.html'
			return render_for_platform(request, template, {'chat': new_chat, 'chat_members': members, 'user': request.user})
		else:
			from django.http import HttpResponseBadRequest
			return HttpResponseBadRequest()


class SendPageMessage(TemplateView):
	""" Пишем сообщения со страниц пользователей или разных списков. Если у пользователя есть друзья,
	    то add_friend_message.html (возможность добавлять друзей), иначе add_message.html
	"""
	template_name = None

	def get(self,request,*args,**kwargs):
		from users.models import User
		from common.template.user import get_settings_template

		if request.user.get_6_friends():
			self.template_name = get_settings_template("chat/message/add_friend_message.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_settings_template("chat/message/add_message.html", request.user, request.META['HTTP_USER_AGENT'])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		return super(SendPageMessage,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from chat.forms import MessageForm

		context = super(SendPageMessage,self).get_context_data(**kwargs)
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
			if request.POST.get('text') or request.POST.get('attach_items'):
				if connections:
					connections += [self.user.pk,]
					_message = Message.create_chat_append_members_and_send_message(creator=request.user, users_ids=connections, text=message.text, voice=request.POST.get('voice'), attach=request.POST.getlist('attach_items'))
				else:
					_message = Message.get_or_create_chat_and_send_message(creator=request.user, repost=None, user=self.user, text=message.text, voice=request.POST.get('voice'), attach=request.POST.getlist('attach_items'))
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
		from common.template.user import get_detect_platform_template
		from chat.models import Message

		self.message, self.template_name = Message.objects.get(uuid=self.kwargs["uuid"]), get_detect_platform_template("chat/message/load_chat_message.html", request.user, request.META['HTTP_USER_AGENT'])
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

		self.message = Message.objects.get(uuid=self.kwargs["uuid"])
		self.chat = self.message.chat
		count, first_message, creator_figure, user_id, self.template_name = self.chat.get_members_count(), self.chat.get_first_message(), '', request.user.pk, get_detect_platform_template("chat/message/load_message.html", request.user, request.META['HTTP_USER_AGENT'])
		if count == 1:
			if self.chat.image:
				figure = '<figure><img src="' + self.chat.image.url + '" style="border-radius:50px;width:50px;" alt="image"></figure>'
			elif self.chat.creator.get_avatar():
				figure = '<figure><img src="' + self.chat.creator.get_avatar() + '" style="border-radius:50px;width:50px;" alt="image"></figure>'
			else:
				figure = '<figure><svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/><path d="M0 0h24v24H0z" fill="none"/></svg></figure>'
			if self.chat.name:
				chat_name = self.chat.name
			else:
				chat_name = self.chat.creator.get_full_name()
			media_body = '<div class="media-body"><h5 class="time-title mb-0">' + chat_name + ' <span class="status bg-success"></span><small class="float-right text-muted">' + first_message.get_created() + '</small></h5><p class="mb-0" style="white-space: nowrap;">' + first_message.get_preview_text() + '</p></div>'
			self.block = '<div class="media">' + figure + media_body + '</div>'
		elif count == 2:
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
			if first_message.creator.user_id == user_id:
				creator_figure = '<span class="underline">Вы:</span> '
			media_body = '<div class="media-body"><h5 class="time-title mb-0">{}{}<small class="float-right text-muted">{}</small></h5><p class="mb-0" style="white-space: nowrap;">{}{}</p></div>'.format(chat_name, status, first_message.get_created(),creator_figure,first_message.get_preview_text())
			self.block = '<div class="media">{}{}{}</div>'.format(figure, media_body, self.chat.get_unread_count_message(user_id))
		elif count > 2:
			if self.chat.image:
				figure = '<figure><img src="' + self.chat.image.url + '"style="border-radius:50px;width:50px;" alt="image"></figure>'
			else:
				figure = '<figure><img src="/static/images/group_chat.jpg" style="border-radius:50px;width:50px;" alt="image"></figure>'
			if self.chat.name:
				chat_name = self.chat.name
			else:
				chat_name = "Групповой чат"
			if first_message.creator.user_id == user_id:
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

class SendMessage(View):
	def post(self,request,*args,**kwargs):
		from common.template.user import render_for_platform
		from chat.models import Message, Chat
		from chat.forms import MessageForm

		chat, form_post = Chat.objects.get(pk=self.kwargs["pk"]), MessageForm(request.POST)
		if request.POST.get('text') or request.POST.get('attach_items'):
			message = form_post.save(commit=False)
			message = Message.send_message(chat=chat, parent=None, creator=request.user, repost=None, text=message.text, voice=request.POST.get('voice'), attach=request.POST.getlist('attach_items'))
			return render_for_platform(request, 'chat/message/message.html', {'object': message})
		else:
			return HttpResponseBadRequest()


class MessageParent(View):
	def post(self, request, *args, **kwargs):
		from common.check.message import check_can_send_message
		from chat.models import Message, Chat
		from chat.forms import MessageForm
		from django.http import HttpResponse

		parent, chat, form_post = Message.objects.get(uuid=self.kwargs["uuid"]), Chat.objects.get(pk=self.kwargs["pk"]), MessageForm(request.POST)
		check_can_send_message(request.user, chat)
		if request.is_ajax() and form_post.is_valid():
			message = form_post.save(commit=False)
			if request.POST.get('text') or request.POST.get('attach_items'):
				new_message = Message.send_message(chat=chat, parent=parent, creator=request.user, repost=None, text=message.text, voice=request.POST.get('voice'), attach=request.POST.getlist('attach_items'))
			return HttpResponse()
		else:
			return HttpResponseBadRequest()


class MessageFixed(View):
	def get(self,request,*args,**kwargs):
		from common.check.message import check_can_send_message
		from chat.models import Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		check_can_send_message(request.user, message.chat)
		if request.is_ajax():
			message.get_fixed_message_for_chat(message.chat.pk)
			return HttpResponse()
		else:
			raise Http404

class MessageUnFixed(View):
	def get(self,request,*args,**kwargs):
		from common.check.message import check_can_send_message
		from chat.models import Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax():
			check_can_send_message(request.user, message.chat)
			message.is_fixed = False
			message.save(update_fields=['is_fixed'])
			return HttpResponse()
		else:
			raise Http404


class MessageFavorite(View):
	def get(self,request,*args,**kwargs):
		from common.check.message import check_can_send_message
		from chat.models import MessageFavorite, Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax():
			check_can_send_message(request.user, message.chat)
			MessageFavorite.create_favorite(request.user.pk, message)
			return HttpResponse()
		else:
			raise Http404

class MessageUnFavorite(View):
	def get(self,request,*args,**kwargs):
		from chat.models import MessageFavorite, Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and MessageFavorite.objects.filter(user_id=request.user.pk, message=message).exists():
			message.is_fixed = False
			message.save(update_fields=['is_fixed'])
			return HttpResponse()
		else:
			raise Http404


class MessageDelete(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and message.creator == request.user:
			message.delete_message()
			return HttpResponse()
		else:
			raise Http404

class MessageRecover(View):
	def get(self,request,*args,**kwargs):
		from chat.models import Message
		from django.http import HttpResponse, Http404

		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and message.creator == request.user:
			message.restore_message()
			return HttpResponse()
		else:
			raise Http404
