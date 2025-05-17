from django.urls import re_path
from managers.view.moderation_list import *

urlpatterns = [
    re_path(r'^user/$', ModerationUserList.as_view()),
    re_path(r'^community/$', ModerationCommunityList.as_view()),
    re_path(r'^post/$', ModerationPostsList.as_view()),
    re_path(r'^photo/$', ModerationPhotoList.as_view()),
    re_path(r'^good/$', ModerationGoodList.as_view()),
    re_path(r'^audio/$', ModerationAudioList.as_view()),
    re_path(r'^video/$', ModerationVideoList.as_view()),
    re_path(r'^doc/$', ModerationDocList.as_view()),
    re_path(r'^planner/$', ModerationPlannerList.as_view()),
    re_path(r'^site/$', ModerationSiteList.as_view()),
    re_path(r'^wiki/$', ModerationWikiList.as_view()),
    re_path(r'^forum/$', ModerationForumList.as_view()),
    re_path(r'^article/$', ModerationArticleList.as_view()),
    re_path(r'^survey/$', ModerationSurveyList.as_view()),
    re_path(r'^mail/$', ModerationMailList.as_view()),
    re_path(r'^message/$', ModerationMessageList.as_view()),
]
