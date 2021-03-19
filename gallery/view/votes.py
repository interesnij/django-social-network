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
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), item.likes_count(), item.dislikes_count()
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = PhotoVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PhotoVotes.LIKE:
                likedislike.vote = PhotoVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=item, user=request.user, vote=PhotoVotes.LIKE)
            result = True
            user_notify(request.user, item.creator.pk, None, "pho"+str(item.pk), "u_post_notify", "LIK")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PhotoUserDislikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), item.likes_count(), item.dislikes_count()
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = PhotoVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PhotoVotes.DISLIKE:
                likedislike.vote = PhotoVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=item, user=request.user, vote=PhotoVotes.DISLIKE)
            result = True
            user_notify(request.user, item.creator.pk, None, "pho"+str(item.pk), "u_post_notify", "DIS")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PhotoCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), comment.likes_count(), comment.dislikes_count()
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = PhotoCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not PhotoCommentVotes.LIKE:
                likedislike.vote = PhotoCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PhotoCommentVotes.DoesNotExist:
            PhotoCommentVotes.objects.create(item=comment, user=request.user, vote=PhotoCommentVotes.LIKE)
            result = True
            if comment.parent:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", pho"+str(comment.parent.photo.pk), "u_photo_comment_notify", "LRE")
            else:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", pho"+str(comment.photo.pk), "u_photo_comment_notify", "LCO")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PhotoCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), comment.likes_count(), comment.dislikes_count()
        if not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        try:
            likedislike = PhotoCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not PhotoCommentVotes.DISLIKE:
                likedislike.vote = PhotoCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PhotoCommentVotes.DoesNotExist:
            PhotoCommentVotes.objects.create(item=comment, user=request.user, vote=PhotoCommentVotes.DISLIKE)
            result = True
            if comment.parent:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", pho"+str(comment.parent.photo.pk), "u_photo_comment_notify", "DRE")
            else:
                user_notify(request.user, comment.commenter.pk, None, "com"+str(comment.pk)+", pho"+str(comment.photo.pk), "u_photo_comment_notify", "DCO")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PhotoCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), item.likes_count(), item.dislikes_count()
        if not item.votes_on or not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = PhotoVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PhotoVotes.LIKE:
                likedislike.vote = PhotoVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=item, user=request.user, vote=PhotoVotes.LIKE)
            result = True
            community_notify(request.user, community, None, "pho"+str(item.pk), "c_photo_notify", "LIK")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PhotoCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), item.likes_count(), item.dislikes_count()
        if not item.votes_on or not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = PhotoVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PhotoVotes.DISLIKE:
                likedislike.vote = PhotoVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=item, user=request.user, vote=PhotoVotes.DISLIKE)
            result = True
            community_notify(request.user, community, None, "pho"+str(item.pk), "c_photo_notify", "DIS")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PhotoCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), comment.likes_count(), comment.dislikes_count()
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = PhotoCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not PhotoCommentVotes.LIKE:
                likedislike.vote = PhotoCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PhotoCommentVotes.DoesNotExist:
            PhotoCommentVotes.objects.create(item=comment, user=request.user, vote=PhotoCommentVotes.LIKE)
            result = True
            if comment.parent:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", pho"+str(comment.parent.photo.pk), "c_photo_comment_notify", "LRE")
            else:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", pho"+str(comment.photo.pk), "c_photo_comment_notify", "LCO")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")


class PhotoCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), comment.likes_count(), comment.dislikes_count()
        if not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        try:
            likedislike = PhotoCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not PhotoCommentVotes.DISLIKE:
                likedislike.vote = PhotoCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except PhotoCommentVotes.DoesNotExist:
            PhotoCommentVotes.objects.create(item=comment, user=request.user, vote=PhotoCommentVotes.DISLIKE)
            result = True
            if comment.parent:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", pho"+str(comment.parent.photo.pk), "c_photo_comment_notify", "DRE")
            else:
                community_notify(request.user, community, None, "com"+str(comment.pk)+", pho"+str(comment.photo.pk), "c_photo_comment_notify", "DCO")
        return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(disliks)}),content_type="application/json")
