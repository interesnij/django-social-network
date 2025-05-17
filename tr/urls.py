from django.urls import re_path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from main.views import SignupView, SwitchView
from users.views.detail import ProfileUserView
from communities.views.details import CommunityDetail


urlpatterns = [
    re_path(r'^logout/$', auth_views.LogoutView.as_view(template_name="account/logout.html"), name='logout'),
    re_path(r'^email-verification/$', TemplateView.as_view(template_name="account/email_verification.html"), name='email-verification'),
    re_path(r'^password-reset/$', TemplateView.as_view(template_name="account/password_reset.html"), name='password-reset'),
    re_path(r'^password-reset/confirm/$', TemplateView.as_view(template_name="account/password_reset_confirm.html"), name='password-reset-confirm'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', TemplateView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    re_path(r'^password-change/$', TemplateView.as_view(template_name="account/password_change.html"), name='password-change'),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^account/', include('allauth.urls')),
    re_path(r'^signup/', SignupView.as_view(), name='signup'),

    re_path(r'^admin/', admin.site.urls),
    re_path(r'', include ('main.urls')),

    re_path(r'^users/', include('users.urls')),
    re_path(r'^posts/', include('posts.urls')),
    re_path(r'^follows/', include('follows.urls')),
    re_path(r'^invitations/', include('invitations.urls')),
    re_path(r'^communities/', include('communities.urls')),
    re_path(r'^friends/', include('frends.urls')),
    re_path(r'^chat/', include('chat.urls')),
    re_path(r'^gallery/', include('gallery.urls')),
    #url(r'^article/', include('article.urls')),
    re_path(r'^goods/', include('goods.urls')),
    re_path(r'^music/', include('music.urls')),
    re_path(r'^video/', include('video.urls')),
    re_path(r'^stat/', include('stst.urls')),
    re_path(r'^questions/', include('quan.urls')),
    re_path(r'^about/', include('about.urls')),
    re_path(r'^managers/', include('managers.urls')),
    re_path(r'^notify/', include('notify.urls')),
    re_path(r'^docs/', include('docs.urls')),
    re_path(r'^survey/', include('survey.urls')),
    re_path(r'^search/', include('search.urls')),

    re_path(r'^public(?P<pk>\d+)/$', CommunityDetail.as_view(), name='community_detail'),
    re_path(r'^id(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),

    re_path(r'^(?P<slug>[\w\-]+)/$', SwitchView.as_view(), name='switch'),
]
