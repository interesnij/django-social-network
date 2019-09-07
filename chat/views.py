from django.views.generic import ListView
from chat.models import Message

class ChatView(ListView):
	template_name="chat.html"
	model=Message
