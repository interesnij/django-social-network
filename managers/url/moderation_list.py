from django.conf.urls import url
from managers.view.moderation_list import *

urlpatterns = [
    url(r'^user/$', ModerationUserList.as_view()),
    url(r'^community/$', ModerationCommunityList.as_view()),
    url(r'^post/$', ModerationPostsList.as_view()),
    url(r'^photo/$', ModerationPhotoList.as_view()),
    url(r'^good/$', ModerationGoodList.as_view()),
    url(r'^audio/$', ModerationAudioList.as_view()),
    url(r'^video/$', ModerationVideoList.as_view()),
    url(r'^doc/$', ModerationDocList.as_view()),
    url(r'^planner/$', ModerationPlannerList.as_view()),
    url(r'^site/$', ModerationSiteList.as_view()),
    url(r'^wiki/$', ModerationWikiList.as_view()),
    url(r'^forum/$', ModerationForumList.as_view()),
    url(r'^article/$', ModerationArticleList.as_view()),
    url(r'^survey/$', ModerationSurveyList.as_view()),
    url(r'^mail/$', ModerationMailList.as_view()),
    url(r'^message/$', ModerationMessageList.as_view()),
]
