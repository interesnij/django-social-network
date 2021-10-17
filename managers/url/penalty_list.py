from django.conf.urls import url
from managers.view.penalty_list import *


urlpatterns = [
    url(r'^user/$', PenaltyUserList.as_view()),
    url(r'^community/$', PenaltyCommunityList.as_view()),
    url(r'^post/$', PenaltyPostsList.as_view()),
    url(r'^photo/$', PenaltyPhotoList.as_view()),
    url(r'^good/$', PenaltyGoodList.as_view()),
    url(r'^audio/$', PenaltyAudioList.as_view()),
    url(r'^video/$', PenaltyVideoList.as_view()),
    url(r'^doc/$', PenaltyDocList.as_view()),
    url(r'^planner/$', PenaltyPlannerList.as_view()),
    url(r'^site/$', PenaltySiteList.as_view()),
    url(r'^wiki/$', PenaltyWikiList.as_view()),
    url(r'^forum/$', PenaltyForumList.as_view()),
    url(r'^article/$', PenaltyArticleList.as_view()),
    url(r'^survey/$', PenaltySurveyList.as_view()),
    url(r'^mail/$', PenaltyMailList.as_view()),
    url(r'^message/$', PenaltyMessageList.as_view()),
]
