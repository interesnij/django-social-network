from users.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from os.path import splitext
import uuid


def upload_to_good_image_directory(good_image, filename):
    good = good_image.good
    return _upload_to_good_directory_directory(good=good, filename=filename)

def _upload_to_good_directory_directory(good, filename):
    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()) + extension

    path = 'goods/%(good_uuid)s/' % {
        'good_uuid': str(good.uuid)}

    return '%(path)s%(new_filename)s' % {'path': path,
                                         'new_filename': new_filename, }
