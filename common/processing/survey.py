def get_survey_processing(survey, type):
    photo.type = type
    photo.save(update_fields=['type'])
    return photo
def get_survey_list_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list
