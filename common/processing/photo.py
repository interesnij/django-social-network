def get_photo_processing(photo, status):
    photo.status = status
    photo.save(update_fields=['status'])
    return photo
def get_photo_list_processing(list, status):
    list.type = status
    list.save(update_fields=['type'])
    return list
def get_photo_comment_processing(comment):
    comment.status = "PUB"
    comment.save(update_fields=['status'])
