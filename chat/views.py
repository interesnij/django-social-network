from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from chat.models import Message
from chat.helpers import ajax_required


class MessagesListView(LoginRequiredMixin,TemplateView):
    template_name = "message_list.html"


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })




class ConversationListView(MessagesListView):
    """CBV to render the inbox, showing an specific conversation with a given
    user, who requires to be active too."""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = self.kwargs["id"]
        return context

    def get_queryset(self):
        active_user = User.objects.get(
            username=self.kwargs["id"])
        return Message.objects.get_conversation(active_user, self.request.user)


@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    sender = request.user
    recipient_id = request.POST.get('to')
    recipient = User.objects.get(id=recipient_id)
    message = request.POST.get('message')
    if len(message.strip()) == 0:
        return HttpResponse()

    if sender != recipient:
        msg = Message.send_message(sender, recipient, message)
        return render(request, 'single_message.html',
                      {'message': msg})

    return HttpResponse()


@login_required
@ajax_required
@require_http_methods(["GET"])
def receive_message(request):
    """Simple AJAX functional view to return a rendered single message on the
    receiver side providing realtime connections."""
    message_id = request.GET.get('message_id')
    message = Message.objects.get(pk=message_id)
    return render(request,
                  'single_message.html', {'message': message})
