from django.conf.urls import url
from main.view.comments import *


urlpatterns = [
    url(r'^list/$', ItemCommentList.as_view()),
    url(r'^likes/$', CommentLikes.as_view()),
    url(r'^dislikes/$', CommentDislikes.as_view()),
]
