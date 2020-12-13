

def get_message_processing(message):
    from chat.models import Message

    message.status = Message.STATUS_DRAFT
    message.save(update_fields=['status'])
    return message
