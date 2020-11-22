from users.models import User
from communities.models import Community
from django.http import HttpResponse, HttpResponseBadRequest
from common.attach.post_attacher import get_post_attach
from common.check.community import check_user_is_staff


def get_message_processing(message):
    from chat.models import Message
    
    message.status = Message.STATUS_DRAFT
    message.save(update_fields=['status'])
    return message
