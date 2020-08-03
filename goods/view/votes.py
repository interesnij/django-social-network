import json
from users.models import User
from goods.models import Good, GoodComment
from communities.models import Community
from django.http import HttpResponse
from django.views import View
from common.model.votes import GoodVotes, GoodCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from rest_framework.exceptions import PermissionDenied
from common.check.community import check_can_get_lists
from django.http import Http404


class GoodUserLikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not good.votes_on or not request.is_ajax():
            raise Http404

        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
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
        if likes != 0:
            like_count = likes
        else:
            like_count = ""
        dislikes = good.dislikes_count()
        if dislikes != 0:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class GoodCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
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
        if likes != 0:
            like_count = likes
        else:
            like_count = ""
        dislikes = comment.dislikes_count()
        if dislikes != 0:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class GoodUserDislikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not good.votes_on or not request.is_ajax():
            raise Http404
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
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
        if likes != 0:
            like_count = likes
        else:
            like_count = ""
        dislikes = good.dislikes_count()
        if dislikes != 0:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class GoodCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
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
        if likes:
            like_count = likes
        else:
            like_count = ""
        dislikes = comment.dislikes_count()
        if dislikes != 0:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class GoodCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
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
        if not request.user.is_staff_of_community_with_name(community.name):
            good.notification_community_like(request.user, community)
        likes = good.likes_count()
        if likes:
            like_count = likes
        else:
            like_count = ""
        dislikes = good.dislikes_count()
        if dislikes:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class GoodCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
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
        if not request.user.is_staff_of_community_with_name(community.name):
            good.notification_community_dislike(request.user, community)
        likes = good.likes_count()
        if likes != 0:
            like_count = likes
        else:
            like_count = ""
        dislikes = good.dislikes_count()
        if dislikes != 0:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


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
        if not request.user.is_staff_of_community_with_name(community.name):
            comment.notification_community_comment_like(request.user, community)
        likes = comment.likes_count()
        if likes:
            like_count = likes
        else:
            like_count = ""
        dislikes = comment.dislikes_count()
        if dislikes:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


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
        if not request.user.is_staff_of_community_with_name(community.name):
            comment.notification_community_comment_dislike(request.user, community)
        likes = comment.likes_count()
        if likes:
            like_count = likes
        else:
            like_count = ""
        dislikes = comment.dislikes_count()
        if dislikes:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")
