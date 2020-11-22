from users.models import User
from chat.models import Message, Chat
from communities.models import Community
from django.http import HttpResponse, HttpResponseBadRequest
from common.attach.post_attacher import get_post_attach
from common.check.community import check_user_is_staff


def get_message_processing(message):
    message.status = Message.STATUS_DRAFT
    message.save(update_fields=['status'])
    return message
