from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.utils.safestring import mark_safe
import json

from chat.models import Message
from chat.helpers import ajax_required


class MessagesListView(LoginRequiredMixin,TemplateView):
    template_name = "message_list.html"


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })




class ConversationListView(MessagesListView):
    """CBV для отображения почтового ящика, показывая конкретный разговор с данным
    пользователь, который тоже должен быть активным."""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = self.kwargs["id"]
        return context

    def get_queryset(self):
        active_user = User.objects.get(
            username=self.kwargs["username"])
        return Message.objects.get_conversation(active_user, self.request.user)


@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """AJAX функциональный вид, чтобы получить только минимальную информацию, процесс
    и создать новое сообщение и вернуть новые данные, которые будут прикреплены к
    поток разговоров."""
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
    """Простой индикатор функциональный вид, чтобы вернуть оказанные одно сообщение на
    сторона приемника обеспечивая соединения в реальном времени."""
    message_id = request.GET.get('message_id')
    message = Message.objects.get(pk=message_id)
    return render(request,
                  'single_message.html', {'message': message})
