import json
from users.models import User
from goods.models import Good, GoodComment
from communities.models import Community
from django.http import HttpResponse
from django.views import View
from common.model.votes import GoodVotes, GoodCommentVotes
from common.check.user import check_user_can_get_list
from rest_framework.exceptions import PermissionDenied
from common.check.community import check_can_get_lists
from django.http import Http404


class GoodUserLikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not good.votes_on or not request.is_ajax():
            raise Http404

        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = GoodVotes.objects.get(parent=good, user=request.user)
            if likedislike.vote is not GoodVotes.LIKE:
                likedislike.vote = GoodVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except GoodVotes.DoesNotExist:
            GoodVotes.objects.create(parent=good, user=request.user, vote=GoodVotes.LIKE)
            result = True
            if user != request.user:
                good.notification_user_like(request.user)
        likes = good.likes_count()
        dislikes = good.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = GoodCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not GoodCommentVotes.LIKE:
                likedislike.vote = GoodCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except GoodCommentVotes.DoesNotExist:
            GoodCommentVotes.objects.create(item=comment, user=request.user, vote=GoodCommentVotes.LIKE)
            result = True
            if user != request.user:
                comment.notification_user_comment_like(request.user)
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodUserDislikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not good.votes_on or not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = GoodVotes.objects.get(parent=good, user=request.user)
            if likedislike.vote is not GoodVotes.DISLIKE:
                likedislike.vote = GoodVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except GoodVotes.DoesNotExist:
            GoodVotes.objects.create(parent=good, user=request.user, vote=GoodVotes.DISLIKE)
            result = True
            if user != request.user:
                good.notification_user_dislike(request.user)
        likes = good.likes_count()
        dislikes = good.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = GoodCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not GoodCommentVotes.DISLIKE:
                likedislike.vote = GoodCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except GoodCommentVotes.DoesNotExist:
            GoodCommentVotes.objects.create(item=comment, user=request.user, vote=GoodCommentVotes.DISLIKE)
            result = True
            if user != request.user:
                comment.notification_user_comment_dislike(request.user)
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not good.votes_on or not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = GoodVotes.objects.get(parent=good, user=request.user)
            if likedislike.vote is not GoodVotes.LIKE:
                likedislike.vote = GoodVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except GoodVotes.DoesNotExist:
            GoodVotes.objects.create(parent=good, user=request.user, vote=GoodVotes.LIKE)
            result = True
            if not request.user.is_staff_of_community(community.pk):
                good.notification_community_like(request.user, community)
        likes = good.likes_count()
        dislikes = good.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not good.votes_on or not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user, community)
        try:
            likedislike = GoodVotes.objects.get(parent=good, user=request.user)
            if likedislike.vote is not GoodVotes.DISLIKE:
                likedislike.vote = GoodVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except GoodVotes.DoesNotExist:
            GoodVotes.objects.create(parent=good, user=request.user, vote=GoodVotes.DISLIKE)
            result = True
            if not request.user.is_staff_of_community(community.pk):
                good.notification_community_dislike(request.user, community)
        likes = good.likes_count()
        dislikes = good.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = GoodCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not GoodCommentVotes.LIKE:
                likedislike.vote = GoodCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except GoodCommentVotes.DoesNotExist:
            GoodCommentVotes.objects.create(item=comment, user=request.user, vote=GoodCommentVotes.LIKE)
            result = True
            if not request.user.is_staff_of_community(community.pk):
                comment.notification_community_comment_like(request.user, community)
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = GoodCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not GoodCommentVotes.DISLIKE:
                likedislike.vote = GoodCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except GoodCommentVotes.DoesNotExist:
            GoodCommentVotes.objects.create(item=comment, user=request.user, vote=GoodCommentVotes.DISLIKE)
            result = True
            if not request.user.is_staff_of_community(community.pk):
                comment.notification_community_comment_dislike(request.user, community)
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")
