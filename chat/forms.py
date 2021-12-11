from chat.models import Chat, Message
from django import forms


class ChatForm(forms.ModelForm):
	class Meta:
		model = Chat
		fields = ['name', 'description', 'type', ]

class MessageForm(forms.ModelForm):
	text=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = Message
		fields = ['text']
