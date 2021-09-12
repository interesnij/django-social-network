def get_message_processing(message, type):
    message.type = type
    message.save(update_fields=['type'])
    return message
def get_edit_message_processing(message):
    return message
def get_chat_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list
