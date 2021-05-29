def get_message_processing(doc, type):
    doc.type = type
    doc.save(update_fields=['type'])
    return doc
def get_chat_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list
