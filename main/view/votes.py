import json
from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment
from communities.models import Community
from django.http import JsonResponse, HttpResponse
from django.views import View
from common.models import ItemVotes, ItemCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import PermissionDenied
from django.core import serializers


class ItemUserLikeWindow(TemplateView):
    template_name="item_votes/like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.item.get_likes_for_item(request.user)
        elif self.user == request.user:
            self.likes = self.item.get_likes_for_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.item.get_likes_for_item(request.user)

        return super(ItemUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemCommunityLikeWindow(TemplateView):
    template_name="item_votes/like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.item.get_likes_for_item(request.user)
        return super(ItemCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemUserCommentLikeWindow(TemplateView):
    template_name="item_votes/comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.comment.get_likes_for_comment_item(request.user)
        elif self.user == request.user:
            self.likes = self.comment.get_likes_for_comment_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.comment.get_likes_for_comment_item(request.user)
        return super(ItemUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemCommunityCommentLikeWindow(TemplateView):
    template_name="item_votes/comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.comment.get_likes_for_comment_item(request.user)
        return super(ItemCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemUserDislikeWindow(TemplateView):
    template_name="item_votes/dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.item.get_dislikes_for_item(request.user)
        elif self.user == request.user:
            self.dislikes = self.item.get_dislikes_for_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.item.get_dislikes_for_item(request.user)

        return super(ItemUserDislikeWindow,self).get(request,*args,**kwargs)


    def get_context_data(self,**kwargs):
        context=super(ItemUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class ItemCommunityDislikeWindow(TemplateView):
    template_name="item_votes/dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.item.get_dislikes_for_item(request.user)
        return super(ItemCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class ItemUserCommentDislikeWindow(TemplateView):
    template_name="item_votes/comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        elif self.user == request.user:
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        return super(ItemUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class ItemCommunityCommentDislikeWindow(TemplateView):
    template_name="item_votes/comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.comment.get_dislikes_for_comment_item(request.user)
        return super(ItemCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class ItemUserLikeCreate(View):
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = ItemVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not ItemVotes.LIKE:
                likedislike.vote = ItemVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_user_like(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.LIKE)
            result = True
        likes = item.get_likes_for_item(request.user)
        if likes.count() != 0:
            like_count = likes.count()
        else:
            like_count = ""
        dislikes = item.get_dislikes_for_item(request.user)
        if dislikes.count() != 0:
            dislike_count = dislikes.count()
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class ItemUserDislikeCreate(View):
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = ItemVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not ItemVotes.DISLIKE:
                likedislike.vote = ItemVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_user_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.DISLIKE)
            result = True
        likes = item.get_likes_for_item(request.user)
        if likes.count() != 0:
            like_count = likes.count()
        else:
            like_count = ""
        dislikes = item.get_dislikes_for_item(request.user)
        if dislikes.count() != 0:
            dislike_count = dislikes.count()
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class ItemCommentUserLikeCreate(View):
    def post(self, request, **kwargs):
        comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = ItemCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not ItemCommentVotes.LIKE:
                likedislike.vote = ItemCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                comment.notification_user_comment_like(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemCommentVotes.DoesNotExist:
            ItemCommentVotes.objects.create(item=comment, user=request.user, vote=ItemCommentVotes.LIKE)
            result = True
        likes = comment.get_likes_for_comment_item(request.user)
        like_count = likes.count()
        dislikes = comment.get_likes_for_comment_item(request.user)
        if dislikes.count() != 0:
            dislike_count = dislikes.count()
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class ItemCommentUserDislikeCreate(View):
    def post(self, request, **kwargs):
        comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = ItemCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not ItemCommentVotes.DISLIKE:
                likedislike.vote = ItemCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                comment.notification_user_comment_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemCommentVotes.DoesNotExist:
            ItemCommentVotes.objects.create(item=comment, user=request.user, vote=ItemCommentVotes.DISLIKE)
            result = True
        likes = comment.get_likes_for_comment_item(request.user)
        if likes.count() != 0:
            like_count = likes.count()
        else:
            like_count = ""
        dislikes = comment.get_likes_for_comment_item(request.user)
        if dislikes.count() != 0:
            dislike_count = dislikes.count()
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class ItemCommunityLikeCreate(View):
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = ItemVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not ItemVotes.LIKE:
                likedislike.vote = ItemVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_community_like(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.LIKE)
            result = True
        likes = item.get_likes_for_item(request.user)
        if likes.count() != 0:
            like_count = likes.count()
        else:
            like_count = ""
        dislikes = item.get_likes_for_item(request.user)
        if dislikes.count() != 0:
            dislike_count = dislikes.count()
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class ItemCommunityDislikeCreate(View):
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = ItemVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not ItemVotes.DISLIKE:
                likedislike.vote = ItemVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_community_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.DISLIKE)
            result = True
        likes = item.get_likes_for_item(request.user)
        if likes.count() != 0:
            like_count = likes.count()
        else:
            like_count = ""
        dislikes = item.get_likes_for_item(request.user)
        if dislikes.count() != 0:
            dislike_count = dislikes.count()
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")

class ItemCommentCommunityLikeCreate(View):
    def post(self, request, **kwargs):
        comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = ItemCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not ItemCommentVotes.LIKE:
                likedislike.vote = ItemCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                comment.notification_community_comment_like(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemCommentVotes.DoesNotExist:
            ItemCommentVotes.objects.create(item=comment, user=request.user, vote=ItemCommentVotes.LIKE)
            result = True
        likes = comment.get_likes_for_comment_item(request.user)
        if likes.count() != 0:
            like_count = likes.count()
        else:
            like_count = ""
        dislikes = comment.get_likes_for_comment_item(request.user)
        if dislikes.count() != 0:
            dislike_count = dislikes.count()
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")


class ItemCommentCommunityDislikeCreate(View):
    def post(self, request, **kwargs):
        comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = ItemCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not ItemCommentVotes.DISLIKE:
                likedislike.vote = ItemCommentVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                comment.notification_community_comment_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemCommentVotes.DoesNotExist:
            ItemCommentVotes.objects.create(item=comment, user=request.user, vote=ItemCommentVotes.DISLIKE)
            result = True
        likes = comment.get_likes_for_comment_item(request.user)
        if likes.count() != 0:
            like_count = likes.count()
        else:
            like_count = ""
        dislikes = comment.get_likes_for_comment_item(request.user)
        if dislikes.count() != 0:
            dislike_count = dislikes.count()
        else:
            dislike_count = ""
        return HttpResponse(json.dumps({"result": result,"like_count": str(like_count),"dislike_count": str(dislike_count)}),content_type="application/json")
