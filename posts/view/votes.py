from users.models import User
from posts.models import Post, PostComment
from communities.models import Community
from django.views import View
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from django.http import Http404


class PostUserLikeCreate(View):
    def get(self, request, **kwargs):
        item, user = Post.objects.get(pk=self.kwargs["post_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return item.send_like(request.user, None)


class PostUserDislikeCreate(View):
    def get(self, request, **kwargs):
        item, user = Post.objects.get(pk=self.kwargs["post_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return item.send_dislike(request.user, None)


class PostCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment, user = PostComment.objects.get(pk=self.kwargs["comment_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return comment.send_like(request.user, None)

class PostCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment, user = PostComment.objects.get(pk=self.kwargs["comment_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return comment.send_dislike(request.user, None)


class PostCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        item, community = Post.objects.get(pk=self.kwargs["post_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user, community)
        return item.send_like(request.user, community)


class PostCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        item, community = Post.objects.get(pk=self.kwargs["post_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() and not item.votes_on:
            raise Http404
        check_can_get_lists(request.user, community)
        return item.send_dislike(request.user, community)


class PostCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment, community = PostComment.objects.get(pk=self.kwargs["comment_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return comment.send_like(request.user, community)


class PostCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment, community = PostComment.objects.get(pk=self.kwargs["comment_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return comment.send_dislike(request.user, community)
