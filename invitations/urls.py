from django.urls import re_path
from invitations.views import InvitationsView


urlpatterns = [
    re_path(r'^invitations/$', InvitationsView.as_view(), name='invitations')
]
