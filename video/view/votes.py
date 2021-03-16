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
from common.notify.video import *


class VideoUserLikeCreate(View):
    def get(self, request, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not video.votes_on:
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = VideoVotes.objects.get(parent=video, user=request.user)
            if likedislike.vote is not VideoVotes.LIKE:
                likedislike.vote = VideoVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except VideoVotes.DoesNotExist:
            VideoVotes.objects.create(parent=video, user=request.user, vote=VideoVotes.LIKE)
            result = True
            user_video_notify(request.user, video.creator.pk, None, video.pk, None, None, "u_video_notify", "L")
        likes = video.likes_count()
        dislikes = video.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class VideoUserDislikeCreate(View):
    def get(self, request, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not video.votes_on:
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = VideoVotes.objects.get(parent=video, user=request.user)
            if likedislike.vote is not VideoVotes.DISLIKE:
                likedislike.vote = VideoVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except VideoVotes.DoesNotExist:
            VideoVotes.objects.create(parent=video, user=request.user, vote=VideoVotes.DISLIKE)
            result = True
            user_video_notify(request.user, video.creator.pk, None, video.pk, None, None, "u_video_notify", "D")
        likes = item.likes_count()
        dislikes = video.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class VideoCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = VideoCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not VideoCommentVotes.LIKE:
                likedislike.vote = VideoCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except VideoCommentVotes.DoesNotExist:
            VideoCommentVotes.objects.create(item=comment, user=request.user, vote=VideoCommentVotes.LIKE)
            result = True
            if comment.parent:
                user_video_notify(request.user, comment.commenter.pk, None, comment.parent.video.pk, comment.pk, None, "u_video_comment_notify", "LR")
            else:
                user_video_notify(request.user, comment.commenter.pk, None, comment.video.pk, comment.pk, None, "u_video_comment_notify", "LC")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class VideoCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = VideoCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not VideoCommentVotes.DISLIKE:
                likedislike.vote = VideoCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except VideoCommentVotes.DoesNotExist:
            VideoCommentVotes.objects.create(item=comment, user=request.user, vote=VideoCommentVotes.DISLIKE)
            result = True
            if comment.parent:
                user_video_notify(request.user, comment.commenter.pk, None, comment.parent.video.pk, comment.pk, None, "u_video_comment_notify", "DR")
            else:
                user_video_notify(request.user, comment.commenter.pk, None, comment.video.pk, comment.pk, None, "u_video_comment_notify", "DC")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class VideoCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not video.votes_on:
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = VideoVotes.objects.get(parent=video, user=request.user)
            if likedislike.vote is not VideoVotes.LIKE:
                likedislike.vote = VideoVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except VideoVotes.DoesNotExist:
            VideoVotes.objects.create(parent=video, user=request.user, vote=VideoVotes.LIKE)
            result = True
            community_video_notify(request.user, community, None, video.pk, None, None, "c_video_notify", "L")
        likes = video.likes_count()
        dislikes = video.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class VideoCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not video.votes_on:
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = VideoVotes.objects.get(parent=video, user=request.user)
            if likedislike.vote is not VideoVotes.DISLIKE:
                likedislike.vote = VideoVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except VideoVotes.DoesNotExist:
            VideoVotes.objects.create(parent=video, user=request.user, vote=VideoVotes.DISLIKE)
            result = True
            community_video_notify(request.user, community, None, video.pk, None, None, "c_video_notify", "D")
        likes = video.likes_count()
        dislikes = item.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class VideoCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = VideoCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not VideoCommentVotes.LIKE:
                likedislike.vote = VideoCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except VideoCommentVotes.DoesNotExist:
            VideoCommentVotes.objects.create(item=comment, user=request.user, vote=VideoCommentVotes.LIKE)
            result = True
            if comment.parent:
                community_video_notify(request.user, community, None, comment.pk, comment.parent.video.pk, None, "c_video_comment_notify", "LR")
            else:
                community_video_notify(request.user, community, None, comment.pk, comment.video.pk, None, "c_video_comment_notify", "LC")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class VideoCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = VideoCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not VideoCommentVotes.DISLIKE:
                likedislike.vote = VideoCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except VideoCommentVotes.DoesNotExist:
            VideoCommentVotes.objects.create(item=comment, user=request.user, vote=VideoCommentVotes.DISLIKE)
            result = True
            if comment.parent:
                community_video_notify(request.user, community, None, comment.pk, comment.parent.video.pk, None, "c_video_comment_notify", "DR")
            else:
                community_video_notify(request.user, community, None, comment.pk, comment.video.pk, None, "c_video_comment_notify", "DC")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")
