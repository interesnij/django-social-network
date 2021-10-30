import uuid
from os.path import splitext


def upload_to_video_directory(user_profile, filename):
    creator = user_profile.creator
    return _upload_to_user_directory(creator=creator, filename=filename)

def _upload_to_user_directory(creator, filename):
    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()) + extension

    path = 'users/%(user_uuid)s/video/' % {
        'user_uuid': str(creator.id)}

    return '%(path)s%(new_filename)s' % {'path': path,
                                         'new_filename': new_filename, }

def validate_file_extension(value):
    import os
    from rest_framework.exceptions import ValidationError
    from django.conf import settings

    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4','.mpeg4']
    if not ext in valid_extensions:
        raise ValidationError('Допустимы форматы: mp4, mpeg4!')
    if value.size > settings.VIDEO_FILE_MAX_SIZE:
        raise ValidationError('Размер не более 10 МБ!')
