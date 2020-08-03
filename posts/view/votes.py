import json
from users.models import User
from posts.models import Post, PostComment
from communities.models import Community
from django.http import HttpResponse
from django.views import View
from common.model.votes import PostVotes, PostCommentVotes
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from django.http import Http404


class PostUserLikeCreate(View):
    def get(self, request, **kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not item.votes_on:
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = PostVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PostVotes.LIKE:
                likedislike.vote = PostVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PostVotes.DoesNotExist:
            PostVotes.objects.create(parent=item, user=request.user, vote=PostVotes.LIKE)
            result = True
        if user != request.user:
            item.notification_user_like(request.user)
        likes = item.likes_count()
        if likes != 0:
            like_count = likes
        else:
            like_count = ""
        dislikes = item.dislikes_count()
        if dislikes != 0:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class PostCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = PostCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not PostCommentVotes.LIKE:
                likedislike.vote = PostCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PostCommentVotes.DoesNotExist:
            PostCommentVotes.objects.create(item=comment, user=request.user, vote=PostCommentVotes.LIKE)
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


class PostUserDislikeCreate(View):
    def get(self, request, **kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not item.votes_on:
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = PostVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PostVotes.DISLIKE:
                likedislike.vote = PostVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PostVotes.DoesNotExist:
            PostVotes.objects.create(parent=item, user=request.user, vote=PostVotes.DISLIKE)
            result = True
        if user != request.user:
            item.notification_user_dislike(request.user)
        likes = item.likes_count()
        if likes != 0:
            like_count = likes
        else:
            like_count = ""
        dislikes = item.dislikes_count()
        if dislikes != 0:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class PostCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = PostCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not PostCommentVotes.DISLIKE:
                likedislike.vote = PostCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PostCommentVotes.DoesNotExist:
            PostCommentVotes.objects.create(item=comment, user=request.user, vote=PostCommentVotes.DISLIKE)
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


class PostCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not item.votes_on:
            raise Http404
        check_can_get_lists(request.user, community)
        try:
            likedislike = PostVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PostVotes.LIKE:
                likedislike.vote = PostVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PostVotes.DoesNotExist:
            PostVotes.objects.create(parent=item, user=request.user, vote=PostVotes.LIKE)
            result = True
        if not request.user.is_staff_of_community_with_name(community.name):
            item.notification_community_like(request.user)
        likes = item.likes_count()
        if likes:
            like_count = likes
        else:
            like_count = ""
        dislikes = item.dislikes_count()
        if dislikes:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class PostCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not item.votes_on:
            raise Http404
        check_can_get_lists(request.user, community)
        try:
            likedislike = PostVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PostVotes.DISLIKE:
                likedislike.vote = PostVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PostVotes.DoesNotExist:
            PostVotes.objects.create(parent=item, user=request.user, vote=PostVotes.DISLIKE)
            result = True
        if not request.user.is_staff_of_community_with_name(community.name):
            item.notification_community_dislike(request.user)
        likes = item.likes_count()
        if likes != 0:
            like_count = likes
        else:
            like_count = ""
        dislikes = item.dislikes_count()
        if dislikes != 0:
            dislike_count = dislikes
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class PostCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = PostCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not PostCommentVotes.LIKE:
                likedislike.vote = PostCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PostCommentVotes.DoesNotExist:
            PostCommentVotes.objects.create(item=comment, user=request.user, vote=PostCommentVotes.LIKE)
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


class PostCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = PostCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not PostCommentVotes.DISLIKE:
                likedislike.vote = PostCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PostCommentVotes.DoesNotExist:
            PostCommentVotes.objects.create(item=comment, user=request.user, vote=PostCommentVotes.DISLIKE)
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
