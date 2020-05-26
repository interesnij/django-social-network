
import uuid
from os.path import splitext


def upload_to_video_directory(user_profile, uuid):
    creator = user_profile.creator
    return _upload_to_user_directory(creator=creator, uuid=uuid)

def _upload_to_user_directory(creator, uuid):
    path = 'users/%(user_id)s/%(image_uuid)s/' % {'user_id': str(creator.id), 'image_uuid': str(uuid)}
    return path
