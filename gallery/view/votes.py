import json
from users.models import User
from gallery.models import Photo, PhotoComment
from communities.models import Community
from django.http import HttpResponse
from django.views import View
from common.model.votes import PhotoVotes, PhotoCommentVotes
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from django.http import Http404
from common.notify.notify import *


class PhotoUserLikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), item.like, item.dislike
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return item.send_like(request.user, None)


class PhotoUserDislikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), item.like, item.dislike
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return item.send_dislike(request.user, None)


class PhotoCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), comment.like, comment.dislike
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return comment.send_like(request.user, None)


class PhotoCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), comment.like, comment.dislike
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return comment.send_dislike(request.user, None)


class PhotoCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), item.like, item.dislike
        if not item.votes_on or not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return item.send_like(request.user, community)


class PhotoCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), item.like, item.dislike
        if not item.votes_on or not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return item.send_dislike(request.user, community)


class PhotoCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), comment.like, comment.dislike
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return comment.send_like(request.user, community)


class PhotoCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), comment.like, comment.dislike
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return comment.send_dislike(request.user, community)
