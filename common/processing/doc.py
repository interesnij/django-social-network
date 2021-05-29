def get_doc_processing(doc, type):
    doc.type = type
    doc.save(update_fields=['type'])
    return doc
def get_doc_list_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list
