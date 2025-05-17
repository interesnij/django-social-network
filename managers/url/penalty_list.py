from django.urls import re_path
from managers.view.penalty_list import *


urlpatterns = [
    re_path(r'^user/$', PenaltyUserList.as_view()),
    re_path(r'^community/$', PenaltyCommunityList.as_view()),
    re_path(r'^post/$', PenaltyPostsList.as_view()),
    re_path(r'^photo/$', PenaltyPhotoList.as_view()),
    re_path(r'^good/$', PenaltyGoodList.as_view()),
    re_path(r'^audio/$', PenaltyAudioList.as_view()),
    re_path(r'^video/$', PenaltyVideoList.as_view()),
    re_path(r'^doc/$', PenaltyDocList.as_view()),
    re_path(r'^planner/$', PenaltyPlannerList.as_view()),
    re_path(r'^site/$', PenaltySiteList.as_view()),
    re_path(r'^wiki/$', PenaltyWikiList.as_view()),
    re_path(r'^forum/$', PenaltyForumList.as_view()),
    re_path(r'^article/$', PenaltyArticleList.as_view()),
    re_path(r'^survey/$', PenaltySurveyList.as_view()),
    re_path(r'^mail/$', PenaltyMailList.as_view()),
    re_path(r'^message/$', PenaltyMessageList.as_view()),
]
