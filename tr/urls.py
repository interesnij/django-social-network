from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from main.views import SignupView, SwitchView
from users.views.detail import ProfileUserView
from communities.views.details import CommunityDetail


urlpatterns = [
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="account/logout.html"), name='logout'),
    url(r'^email-verification/$', TemplateView.as_view(template_name="account/email_verification.html"), name='email-verification'),
    url(r'^password-reset/$', TemplateView.as_view(template_name="account/password_reset.html"), name='password-reset'),
    url(r'^password-reset/confirm/$', TemplateView.as_view(template_name="account/password_reset_confirm.html"), name='password-reset-confirm'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', TemplateView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    url(r'^password-change/$', TemplateView.as_view(template_name="account/password_change.html"), name='password-change'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^signup/', SignupView.as_view(), name='signup'),

    url(r'^admin/', admin.site.urls),
    url(r'', include ('main.urls')),

    url(r'^users/', include('users.urls')),
    url(r'^posts/', include('posts.urls')),
    url(r'^follows/', include('follows.urls')),
    url(r'^invitations/', include('invitations.urls')),
    url(r'^communities/', include('communities.urls')),
    url(r'^friends/', include('frends.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^article/', include('article.urls')),
    url(r'^goods/', include('goods.urls')),
    url(r'^music/', include('music.urls')),
    url(r'^video/', include('video.urls')),
    url(r'^stat/', include('stst.urls')),
    url(r'^questions/', include('quan.urls')),
    url(r'^about/', include('about.urls')),
    url(r'^logs/', include('logs.urls')),
    url(r'^managers/', include('managers.urls')),
    url(r'^notify/', include('notify.urls')),
    url(r'^docs/', include('docs.urls')),
    url(r'^survey/', include('survey.urls')),
    url(r'^search/', include('search.urls')),

    url(r'^public(?P<pk>\d+)/$', CommunityDetail.as_view(), name='community_detail'),
    url(r'^id(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),

    url(r'^(?P<slug>[\w\-]+)/$', SwitchView.as_view(), name='switch'),
]
