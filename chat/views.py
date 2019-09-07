from django.views.generic import ListView


class ChatView(ListView):
	template_name="chat.html"
