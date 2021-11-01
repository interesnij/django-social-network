import json
from users.models import User
from video.models import Video, VideoComment
from communities.models import Community
from django.http import HttpResponse
from django.views import View
from common.model.votes import VideoVotes, VideoCommentVotes
from rest_framework.exceptions import PermissionDenied
from common.check.community import check_can_get_lists
from django.http import Http404
from common.notify.notify import *


class VideoUserLikeCreate(View):
    def get(self, request, **kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not video.votes_on:
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return video.send_like(request.user, None)


class VideoUserDislikeCreate(View):
    def get(self, request, **kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not video.votes_on:
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return video.send_dislike(request.user, None)


class VideoCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return comment.send_like(request.user, None)


class VideoCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return comment.send_dislike(request.user, None)


class VideoCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not video.votes_on:
            raise Http404
        check_can_get_lists(request.user,community)
        return video.send_like(request.user, community)


class VideoCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not video.votes_on:
            raise Http404
        check_can_get_lists(request.user,community)
        return video.send_dislike(request.user, community)


class VideoCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return comment.send_like(request.user, community)


class VideoCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return comment.send_dislike(request.user, community)
