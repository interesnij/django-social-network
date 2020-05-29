from django.conf.urls import url
from about.views import AboutView, TermsView, PolicyView, LicenceView


urlpatterns = [
    url(r'^$', AboutView.as_view(), name='about'),
    url(r'^terms/$', TermsView.as_view(), name='terms'),
    url(r'^policy$', PolicyView.as_view(), name='policy'),
    url(r'^licence/$', LicenceView.as_view(), name='licence'),
]
