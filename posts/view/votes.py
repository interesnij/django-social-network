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
from common.notify.notify import *


class PostUserLikeCreate(View):
    def get(self, request, **kwargs):
        item, user = Post.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return item.send_like(request.user, None)


class PostUserDislikeCreate(View):
    def get(self, request, **kwargs):
        item, user = Post.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
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
            user_notify(request.user, item.creator.pk, None, "pos"+str(item.pk), "u_post_notify", "DIS")
        likes = item.likes_count()
        dislikes = item.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PostCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment, user = PostComment.objects.get(pk=self.kwargs["comment_pk"]), User.objects.get(pk=self.kwargs["pk"])
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
            if comment.parent:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", pos"+str(comment.parent.post.pk), "u_post_comment_notify", "LRE")
            else:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", pos"+str(comment.post.pk), "u_post_comment_notify", "LCO")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")

class PostCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment, user = PostComment.objects.get(pk=self.kwargs["comment_pk"]), User.objects.get(pk=self.kwargs["pk"])
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
            if comment.parent:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", pos"+str(comment.parent.post.pk), "u_post_comment_notify", "DRE")
            else:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", pos"+str(comment.post.pk), "u_post_comment_notify", "DCO")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PostCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        item, community = Post.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
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
            community_notify(request.user, community, None, "pos"+str(item.pk), "c_post_notify", "LIK")
        likes = item.likes_count()
        dislikes = item.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PostCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        item, community = Post.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
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
            community_notify(request.user, community, None, "pos"+str(item.pk), "c_post_notify", "DIS")
        likes = item.likes_count()
        dislikes = item.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PostCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment, community = PostComment.objects.get(pk=self.kwargs["comment_pk"]), Community.objects.get(pk=self.kwargs["pk"])
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
            if comment.parent:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", pos"+str(comment.parent.post.pk), "c_post_comment_notify", "LRE")
            else:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", pos"+str(comment.post.pk), "c_post_comment_notify", "LCO")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PostCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment, community = PostComment.objects.get(pk=self.kwargs["comment_pk"]), Community.objects.get(pk=self.kwargs["pk"])
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
            if comment.parent:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", pos"+str(comment.parent.post.pk), "c_post_comment_notify", "DRE")
            else:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", pos"+str(comment.post.pk), "c_post_comment_notify", "DCO")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")
