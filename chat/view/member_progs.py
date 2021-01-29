from chat.models import Chat


""" ListView """
from django.views.generic import ListView
class ChatMembers(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.template.user import get_settings_template

		self.chat, self.template_name = Chat.objects.get(pk=self.kwargs["pk"]), get_settings_template("chat/chat/members.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(ChatMembers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ChatMembers,self).get_context_data(**kwargs)
		context["chat"] = self.chat
		return context

	def get_queryset(self):
		members = self.chat.get_members(self.chat)
		return members


""" View """
from django.views import View

class ChatMemberCreate(View):
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

class ChatMemberDelete(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from chat.models import ChatUsers
		from django.http import HttpResponse

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax():
			ChatUsers.delete_membership(user=user, chat=chat)
			return HttpResponse()
		else:
			raise Http404


class ChatAdminCreate(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from django.http import HttpResponse

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax() and request.user.is_administrator_of_chat(chat.pk):
			new_admin = chat.add_administrator(user)
			return HttpResponse()
		else:
			raise Http404

class ChatAdminDelete(View):
	def get(self,request,*args,**kwargs):
		from users.models import User
		from django.http import HttpResponse

		chat, user = Chat.objects.get(pk=self.kwargs["pk"]), User.objects.get(pk=self.kwargs["user_pk"])
		if request.is_ajax() and request.user.is_administrator_of_chat(chat.pk):
			new_admin = chat.remove_administrator(user)
			return HttpResponse()
		else:
			raise Http404
