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
from common.notify.notify import *


class GoodUserLikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), good.likes_count(), good.dislikes_count()
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
            user_notify(request.user, good.creator.pk, None, "goo"+str(good.pk), "u_good_notify", "LIK")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodUserDislikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), good.likes_count(), good.dislikes_count()
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
            user_notify(request.user, good.creator.pk, None, "goo"+str(good.pk), "u_good_notify", "DIS")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), comment.likes_count(), comment.dislikes_count()
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
            if comment.parent:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", goo"+str(comment.parent.good.pk), "u_post_comment_notify", "LRE")
            else:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", goo"+str(comment.good.pk), "u_post_comment_notify", "LCO")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), comment.likes_count(), comment.dislikes_count()
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
            if comment.parent:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", goo"+str(comment.parent.good.pk), "u_post_comment_notify", "DRE")
            else:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", goo"+str(comment.good.pk), "u_post_comment_notify", "DCO")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), good.likes_count(), good.dislikes_count()
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
            community_notify(request.user, good.creator.pk, None, "goo"+str(good.pk), "c_good_notify", "LIK")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), good.likes_count(), good.dislikes_count()
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
            community_notify(request.user, good.creator.pk, None, "goo"+str(good.pk), "c_good_notify", "DIS")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), comment.likes_count(), comment.dislikes_count()
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
            if comment.parent:
                community_post_notify(request.user, community, None, "com"+str(comment.pk)+", goo"+str(comment.parent.good.pk), "c_good_comment_notify", "LRE")
            else:
                community_post_notify(request.user, community, None, "com"+str(comment.pk)+", goo"+str(comment.good.pk), "c_good_comment_notify", "LCO")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class GoodCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), comment.likes_count(), comment.dislikes_count()
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
            if comment.parent:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", goo"+str(comment.parent.good.pk), "c_good_comment_notify", "DRE")
            else:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", goo"+str(comment.good.pk), "c_good_comment_notify", "DCO")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")
