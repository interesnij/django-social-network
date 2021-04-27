def get_doc_processing(doc, status):
    doc.status = status
    doc.save(update_fields=['status'])
    return doc
def get_doc_list_processing(list, status):
    list.type = status
    list.save(update_fields=['type'])
    return list
