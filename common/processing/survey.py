def get_survey_processing(survey, status):
    photo.status = status
    photo.save(update_fields=['status'])
    return photo
def get_survey_list_processing(list, status):
    list.type = status
    list.save(update_fields=['type'])
    return list
