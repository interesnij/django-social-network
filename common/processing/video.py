def get_video_processing(video, type):
    video.type = type
    video.save(update_fields=['type'])
    return video
def get_video_list_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list
