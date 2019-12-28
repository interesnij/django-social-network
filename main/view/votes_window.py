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


#перезагрузка окна с последними лайками для записи пользователя
class ItemUserLikeWindow(TemplateView):
    template_name="item_votes/u_like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.item.get_likes_for_item(request.user)[0:6]
        elif self.user == request.user:
            self.likes = self.item.get_likes_for_item(request.user)[0:6]
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.item.get_likes_for_item(request.user)[0:6]
        return super(ItemUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

#перезагрузка окна с последними дизлайками для записи пользователя
class ItemUserCommentLikeWindow(TemplateView):
    template_name="item_votes/u_comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        elif self.user == request.user:
            self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        return super(ItemUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

#перезагрузка окна с последними лайками для комментария записи пользователя
class ItemUserDislikeWindow(TemplateView):
    template_name="item_votes/u_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        elif self.user == request.user:
            self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        return super(ItemUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

#перезагрузка окна с последними дизлайками для комментария записи пользователя
class ItemUserCommentDislikeWindow(TemplateView):
    template_name="item_votes/u_comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        elif self.user == request.user:
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        return super(ItemUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


#перезагрузка окна с последними лайками для записи сообщества
class ItemCommunityLikeWindow(TemplateView):
    template_name="item_votes/c_like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.item.get_likes_for_item(request.user)[0:6]
        return super(ItemCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

#перезагрузка окна с последними дизлайками для записи сообщества
class ItemCommunityDislikeWindow(TemplateView):
    template_name="item_votes/c_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        return super(ItemCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

#перезагрузка окна с последними лайками для комментария записи сообщества
class ItemCommunityCommentLikeWindow(TemplateView):
    template_name="item_votes/c_comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        return super(ItemCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

#перезагрузка окна с последними дизлайками для комментария записи сообщества
class ItemCommunityCommentDislikeWindow(TemplateView):
    template_name="item_votes/c_comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        return super(ItemCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


#Окно со всеми лайками для записи пользователя
class AllItemUserLikeWindow(TemplateView):
    template_name="item_votes/u_all_like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.item.get_likes_for_item(request.user)
        elif self.user == request.user:
            self.likes = self.item.get_likes_for_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.item.get_likes_for_item(request.user)
        return super(AllItemUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

#Окно со всеми дизлайками для записи пользователя
class AllItemUserDislikeWindow(TemplateView):
    template_name="item_votes/u_all_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.item.get_dislikes_for_item(request.user)
        elif self.user == request.user:
            self.dislikes = self.item.get_dislikes_for_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.item.get_dislikes_for_item(request.user)
        return super(AllItemUserDislikeWindow,self).get(request,*args,**kwargs)
    def get_context_data(self,**kwargs):
        context=super(AllItemUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

#Окно со всеми дизлайками для комментария записи пользователя
class AllItemUserCommentDislikeWindow(TemplateView):
    template_name="item_votes/u_all_comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        elif self.user == request.user:
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        return super(AllItemUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

#Окно со всеми лайками для комментария записи пользователя
class AllItemUserCommentLikeWindow(TemplateView):
    template_name="item_votes/u_all_comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.comment.get_likes_for_comment_item(request.user)
        elif self.user == request.user:
            self.likes = self.comment.get_likes_for_comment_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.comment.get_likes_for_comment_item(request.user)
        return super(AllItemUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


#Окно со всеми лайками для записи сообщества
class AllItemCommunityLikeWindow(TemplateView):
    template_name="item_votes/c_all_like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.item.get_likes_for_item(request.user)
        return super(AllItemCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

#Окно со всеми дизлайками для записи сообщества
class AllItemCommunityDislikeWindow(TemplateView):
    template_name="item_votes/c_all_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.item.get_dislikes_for_item(request.user)
        return super(AllItemCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

#Окно со всеми лайками для комментария к записи сообщества
class AllItemCommunityCommentLikeWindow(TemplateView):
    template_name="item_votes/c_all_comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.comment.get_likes_for_comment_item(request.user)
        return super(AllItemCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

#Окно со всеми дизлайками для комментирия к записи сообщества
class AllItemCommunityCommentDislikeWindow(TemplateView):
    template_name="item_votes/c_all_comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        return super(AllItemCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

#Окно со всеми поделившимися записью пользователя
class AllItemUserRepostWindow(TemplateView):
    template_name="item_votes/u_all_repost_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.reposts = self.item.get_reposts()
        elif self.user == request.user:
            self.reposts = self.item.get_reposts()
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.reposts = self.item.get_reposts()
        return super(AllItemUserRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemUserRepostWindow,self).get_context_data(**kwargs)
        context["reposts"]=self.reposts
        return context

#Окно со всеми поделившимися записью сообщества
class AllItemCommunityRepostWindow(TemplateView):
    template_name="item_votes/c_all_repost_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.reposts = self.item.get_reposts()
        return super(AllItemCommunityRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AllItemCommunityRepostWindow,self).get_context_data(**kwargs)
        context["reposts"]=self.reposts
        return context
