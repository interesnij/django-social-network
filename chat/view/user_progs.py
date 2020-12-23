from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from chat.forms import ChatForm, MessageForm
from chat.models import Chat, Message, MessageFavorite
from users.models import User
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.attach.message_attacher import get_message_attach
from common.template.user import get_settings_template, render_for_platform, get_detect_platform_template
from common.check.message import check_can_send_message


class SendPageMessage(TemplateView):
	""" Пишем сообщения со страниц пользователей или разных списков. Если у пользователя есть друзья,
	    то add_friend_message.html (возможность добавлять друзей), иначе add_message.html
	"""
	template_name = None

	def get(self,request,*args,**kwargs):
		if request.user.get_6_friends():
			self.template_name = get_settings_template("chat/message/add_friend_message.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_settings_template("chat/message/add_message.html", request.user, request.META['HTTP_USER_AGENT'])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		return super(SendPageMessage,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(SendPageMessage,self).get_context_data(**kwargs)
		context["form"] = MessageForm()
		context["member"] = self.user
		return context

	def post(self,request,*args,**kwargs):
		self.form, self.user, connections = MessageForm(request.POST), User.objects.get(pk=self.kwargs["pk"]), request.POST.getlist("chat_items")
		check_user_can_get_list(request.user, self.user)

		if request.is_ajax() and self.form.is_valid():
			message = self.form.save(commit=False)
			if request.POST.get('text') or request.POST.get('photo') or \
				request.POST.get('video') or request.POST.get('music') or \
				request.POST.get('good') or request.POST.get('article') or \
				request.POST.get('playlist') or request.POST.get('video_list') or \
				request.POST.get('photo_list') or request.POST.get('doc_list') or \
				request.POST.get('doc') or request.POST.get('good_list'):
				if connections:
					connections += [self.user.pk,]
					_message = Message.create_chat_append_members_and_send_message(creator=request.user, users_ids=connections, text=message.text)
					get_message_attach(request, _message)
				else:
					_message = Message.get_or_create_chat_and_send_message(creator=request.user, repost=None, user=self.user, text=message.text)
					get_message_attach(request, _message)
				return HttpResponse()
			else:
				return HttpResponseBadRequest()


class LoadUserChatMessage(TemplateView):
	""" Отрисовываем новое сообщение для всех участников чата, кроме текущего (это фильтруем в socket.js) - он его и так увидит сразу.
		Отрисовываем на странице чата.
	"""
	template_name = None
	def get(self,request,*args,**kwargs):
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


class SendMessage(View):
	def post(self,request,*args,**kwargs):
		chat, form_post = Chat.objects.get(pk=self.kwargs["pk"]), MessageForm(request.POST)
		if request.POST.get('text') or request.POST.get('voice') or request.POST.get('photo') or \
			request.POST.get('video') or request.POST.get('music') or \
			request.POST.get('good') or request.POST.get('article') or \
			request.POST.get('playlist') or request.POST.get('video_list') or \
			request.POST.get('photo_list') or request.POST.get('doc_list') or \
			request.POST.get('doc') or request.POST.get('good_list'):
			message = form_post.save(commit=False)
			message = Message.send_message(chat=chat, parent=None, creator=request.user, repost=None, text=message.text, voice=request.POST.get('voice'))
			get_message_attach(request, message)
			return render_for_platform(request, 'chat/message/message.html', {'object': message})
		else:
			return HttpResponseBadRequest()


class MessageParent(View):
    def post(self, request, *args, **kwargs):
        parent, chat, form_post = Message.objects.get(uuid=self.kwargs["uuid"]), Chat.objects.get(pk=self.kwargs["pk"]), MessageForm(request.POST)
        check_can_send_message(request.user, chat)
        if request.is_ajax() and form_post.is_valid():
            message = form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('photo') or \
                request.POST.get('video') or request.POST.get('music') or \
                request.POST.get('good') or request.POST.get('article') or \
                request.POST.get('playlist') or request.POST.get('video_list') or \
                request.POST.get('photo_list') or request.POST.get('doc_list') or \
                request.POST.get('doc') or request.POST.get('good_list'):
            	new_message = Message.send_message(chat=chat, parent=parent, creator=request.user, repost=None, text=message.text)
            	get_post_attach(request, new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class MessageFixed(View):
	def get(self,request,*args,**kwargs):
		message = Message.objects.get(uuid=self.kwargs["uuid"])
		check_can_send_message(request.user, message.chat)
		if request.is_ajax():
			message.get_fixed_message_for_chat(message.chat.pk)
			return HttpResponse()
		else:
			raise Http404

class MessageUnFixed(View):
	def get(self,request,*args,**kwargs):
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
		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax():
			check_can_send_message(request.user, message.chat)
			MessageFavorite.create_favorite(request.user.pk, message)
			return HttpResponse()
		else:
			raise Http404

class MessageUnFavorite(View):
	def get(self,request,*args,**kwargs):
		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and MessageFavorite.objects.filter(user_id=request.user.pk, message=message).exists():
			message.is_fixed = False
			message.save(update_fields=['is_fixed'])
			return HttpResponse()
		else:
			raise Http404


class MessageDelete(View):
	def get(self,request,*args,**kwargs):
		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and message.creator == request.user:
			message.is_deleted = True
			message.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404

class MessageAbortDelete(View):
	def get(self,request,*args,**kwargs):
		message = Message.objects.get(uuid=self.kwargs["uuid"])
		if request.is_ajax() and message.creator == request.user:
			message.is_deleted = False
			message.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404
