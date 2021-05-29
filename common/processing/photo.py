def get_photo_processing(photo, type):
    photo.type = type
    photo.save(update_fields=['type'])
    return photo
def get_photo_list_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list
def get_photo_comment_processing(comment):
    comment.type = "PUB"
    comment.save(update_fields=['type'])
