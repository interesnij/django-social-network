from django.urls import re_path
from about.views import AboutView, TermsView, PolicyView, LicenceView


urlpatterns = [
    re_path(r'^$', AboutView.as_view(), name='about'),
    re_path(r'^terms/$', TermsView.as_view(), name='terms'),
    re_path(r'^privacy$', PolicyView.as_view(), name='policy'),
    re_path(r'^licence/$', LicenceView.as_view(), name='licence'),
]
