import json
from users.models import User
from gallery.models import Photo, PhotoComment
from communities.models import Community
from django.http import HttpResponse
from django.views import View
from common.model.votes import PhotoVotes, PhotoCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id, check_can_get_posts_for_community_with_name
from rest_framework.exceptions import PermissionDenied
from notifications.model2.item import item_community_notification_handler, ItemCommunityNotification
from rest_framework.exceptions import PermissionDenied


class PhotoUserLikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not item.votes_on:
            raise PermissionDenied('Реакции отключены.')

        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
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


class PhotoCommentUserLikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
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


class PhotoUserDislikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if not item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
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


class PhotoCommentUserDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
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


class PhotoCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        check_can_get_posts_for_community_with_name(request.user,community.name)
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
        if not request.user.is_staff_of_community_with_name(community.name):
            item.notification_community_like(request.user, community)
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


class PhotoCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        item = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if not item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        check_can_get_posts_for_community_with_name(request.user,community.name)
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
        if not request.user.is_staff_of_community_with_name(community.name):
            item.notification_community_dislike(request.user, community)
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


class PhotoCommentCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
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


class PhotoCommentCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
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
