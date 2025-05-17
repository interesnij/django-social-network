from django.urls import re_path
from main.view.comments import *


urlpatterns = [
    re_path(r'^list/$', ItemCommentList.as_view()),
    re_path(r'^likes/$', CommentLikes.as_view()),
    re_path(r'^dislikes/$', CommentDislikes.as_view()),
]
