import uuid
from os.path import splitext


def upload_to_community_avatar_directory(community, filename):
    return _upload_to_community_directory(community=community, filename=filename)

def upload_to_community_b_avatar_directory(community, filename):
    return _upload_to_community_directory_2(community=community, filename=filename)


def upload_to_community_cover_directory(community, filename):
    return _upload_to_community_directory(community=community, filename=filename)


def _upload_to_community_directory(community, filename):
    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()) + extension
    path = 'communities/%(community_id)s/' % {'community_id': str(community.id)}
    return '%(path)s%(new_filename)s' % {'path': path,'new_filename': new_filename, }


def _upload_to_community_directory_2(community, filename):
    from communities.models import Community

    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()) + extension
    community_2 = Community.objects.get(community=community)
    path = 'communities/%(community_id)s/' % {'community_id': str(community_2.id)}
    return '%(path)s%(new_filename)s' % {'path': path,'new_filename': new_filename, }
