from django.views.generic.base import TemplateView
from chat.models import Chat, ChatUsers
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from chat.forms import ChatForm
from users.models import User
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform
from common.check.message import check_can_change_chat


class CreateChat(TemplateView):
	""" если у инициатора нет друзей, показываем форму пустого чата. Если есть, то с возможностью добавлять друзей в чат.
	    Третий и четвертый варианты - пока не понятны, но зачем то я их задумал. Пока не ясно, что я хотел этим сказать
	"""
	template_name = None
	member = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if self.user != request.user:
			self.member = self.user

		if self.user == request.user and not request.user.get_6_friends():
			self.template_name = get_settings_template("chat/chat/create_chat_empty.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.user == request.user and request.user.get_6_friends():
			self.template_name = get_settings_template("chat/chat/create_chat_with_members.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.user != request.user and not request.user.get_6_friends():
			self.template_name = get_settings_template("chat/chat/create_chat_send_message.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.user != request.user and request.user.get_6_friends():
			self.template_name = get_settings_template("chat/chat/create_chat_send_message_with_members.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CreateChat,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CreateChat,self).get_context_data(**kwargs)
		context["form"] = ChatForm()
		context["member"] = self.user
		return context

	def post(self,request,*args,**kwargs):
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
			HttpResponseBadRequest()


class ChatDelete(View):
	def get(self,request,*args,**kwargs):
		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			check_can_change_chat(request.user, chat)
			chat.is_deleted = True
			message.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404

class ChatAbortDelete(View):
	def get(self,request,*args,**kwargs):
		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			check_can_change_chat(request.user, chat)
			chat.is_deleted = False
			message.save(update_fields=['is_deleted'])
			return HttpResponse()
		else:
			raise Http404


class ChatExit(View):
	def get(self,request,*args,**kwargs):
		chat = Chat.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			ChatUsers.delete_membership(request.user, chat)
			return HttpResponse()
		else:
			raise Http404
