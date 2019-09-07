from django.views.generic import ListView
from users.models import User


class ChatView(ListView):
	template_name="chat.html"
	model=User
