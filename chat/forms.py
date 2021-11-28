from chat.models import Chat, Message
from django import forms


class ChatForm(forms.ModelForm):
	class Meta:
		model = Chat
		fields = ['name', 'image', 'description', 'can_add_members', 'can_edit_info', 'can_fix_item', 'can_mention', 'can_add_admin', 'can_add_design']

class MessageForm(forms.ModelForm):
	text=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control text-comment form-control-rounded'}))

	class Meta:
		model = Message
		fields = ['text']
