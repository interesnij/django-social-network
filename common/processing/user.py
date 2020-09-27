from users.model.settings import *
from users.model.list import *
from users.model.profile import *


def create_user_models(user):

    try:
        UserProfileFamily.objects.get(user=user)
    except:
        UserProfileFamily.objects.create(user=user)
    try:
        UserProfileAnketa.objects.get(user=user)
    except:
        UserProfileAnketa.objects.create(user=user)
