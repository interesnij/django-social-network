import uuid
from os.path import splitext


def upload_to_photo_directory(file, filename):
    return _upload_to_photo_directory(file=file, filename=filename)


def _upload_to_photo_directory(photo, filename):
    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()) + extension

    path = 'photo/%(photo_uuid)s/' % {
        'photo_uuid': str(photo.id)}

    return '%(path)s%(new_filename)s' % {'path': path,
                                         'new_filename': new_filename, }
