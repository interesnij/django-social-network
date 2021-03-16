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
from common.notify.post import *


class PostUserLikeCreate(View):
    def get(self, request, **kwargs):
        item, user = Post.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
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
            user_post_notify(request.user, item.creator.pk, None, item.pk, None, None, "u_post_notify", "L")
        likes = item.likes_count()
        dislikes = item.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


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
            user_post_notify(request.user, item.creator.pk, None, item.pk, None, None, "u_post_notify", "D")
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
                user_post_notify(request.user, comment.commenter.pk, None, comment.parent.post.pk, comment.pk, None, "u_post_comment_notify", "LR")
            else:
                user_post_notify(request.user, comment.commenter.pk, None, comment.post.pk, comment.pk, None, "u_post_comment_notify", "LC")
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
                user_post_notify(request.user, comment.commenter.pk, None, comment.parent.post.pk, comment.pk, None, "u_post_comment_notify", "DR")
            else:
                user_post_notify(request.user, comment.commenter.pk, None, comment.post.pk, comment.pk, None, "u_post_comment_notify", "DC")
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
            community_post_notify(request.user, community, None, item.pk, None, None, "c_post_notify", "L")
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
            community_post_notify(request.user, community, None, item.pk, None, None, "c_post_notify", "D")
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
                community_post_notify(request.user, community, None, comment.pk, comment.parent.post.pk, None, "c_post_comment_notify", "LR")
            else:
                community_post_notify(request.user, community, None, comment.pk, comment.post.pk, None, "c_post_comment_notify", "LC")
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
                community_post_notify(request.user, community, None, comment.pk, comment.parent.post.pk, None, "c_post_comment_notify", "DR")
            else:
                community_post_notify(request.user, community, None, comment.pk, comment.post.pk, None, "c_post_comment_notify", "DC")
        likes = comment.likes_count()
        dislikes = comment.dislikes_count()
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")
