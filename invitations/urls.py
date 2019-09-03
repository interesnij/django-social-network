from django.conf.urls import url
from invitations.views import InvitationsView


urlpatterns = [
    url(r'^invitations/$', InvitationsView.as_view(), name='invitations')
]
