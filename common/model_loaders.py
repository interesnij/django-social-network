from django.apps import apps

def get_user_model():
    return apps.get_model('users.User')

def get_community_model():
    return apps.get_model('communities.Community')
