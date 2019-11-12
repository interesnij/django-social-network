from django.views.generic.base import TemplateView
from users.models import User
from posts.models import Post
from main.models import Item
from frends.models import Connect
from follows.models import Follow
from goods.models import Good
from communities.models import Community
from main.forms import CommentForm
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from generic.mixins import EmojiListMixin
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


class UserItemView(EmojiListMixin, TemplateView):
    model=Item
    template_name="lenta/user_item.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(uuid=self.kwargs["uuid"])
        request_user = request.user
        if self.user != request_user:
            check_is_not_blocked_with_user_with_id(user=request_user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request_user, user_id=self.user.id)
        self.items = self.user.get_posts()
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()
        self.item.views += 1
        self.item.save()
        return super(UserItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserItemView,self).get_context_data(**kwargs)
        context["object"]=self.item
        context["user"]=self.user
        context["next"]=self.next
        context["prev"]=self.prev
        return context


class AvatarReload(TemplateView):
    template_name="profile/avatar_reload.html"


class ItemListView(ListView, EmojiListMixin):
    template_name="lenta/item_list.html"
    model=Item
    paginate_by=6

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        request_user = request.user
        if self.user != request_user:
            check_is_not_blocked_with_user_with_id(user=request_user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request_user, user_id=self.user.id)
        self.items = self.user.get_posts()
        return super(ItemListView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemListView,self).get_context_data(**kwargs)
        context["user"]=self.user
        context["items"]=self.items
        return context


class AllUsers(ListView):
    template_name="all_users.html"
    model=User

    def get_queryset(self):
        users=User.objects.only('id')
        return users


class ProfileUserView(TemplateView):
    template_name = 'user.html'

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        try:
            self.is_frend = request.user.is_connected_with_user(self.user)
        except:
            self.is_frend = None
        self.communities=Community.objects.filter(memberships__user__id=self.user.pk)[0:5]
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['form_avatar'] = AvatarUserForm()
        context['form_comment'] = CommentForm()
        context['communities'] = self.communities
        context['is_frend'] = self.is_frend
        return context


class ProfileReload(TemplateView):
    template_name = 'user_reload.html'

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.communities=Community.objects.filter(memberships__user__id=self.user.pk)[0:5]
        return super(ProfileReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['form_avatar'] = AvatarUserForm()
        context['form_comment'] = CommentForm()
        context['communities'] = self.communities
        return context


class ProfileButtonReload(TemplateView):
    template_name="profile_button.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        try:
            self.connect = Connect.objects.get(user=self.request.user,target_user=self.user)
        except:
            self.connect = None
        try:
            self.follow = Follow.objects.get(followed_user=self.user,user=self.request.user)
        except:
            self.follow = None
        try:
            self.follow2 = Follow.objects.get(followed_user=self.request.user,user=self.user)
        except:
            self.follow2 = None

        return super(ProfileButtonReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileButtonReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['connect'] = self.connect
        context['follow'] = self.follow
        context['follow2'] = self.follow2
        return context


class ProfileStatReload(TemplateView):
    template_name="profile_stat.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.follows_count=self.user.count_following()
        self.goods_count=self.user.count_goods()
        self.connect_count=self.user.count_connections()
        self.communities_count=self.user.count_community()
        return super(ProfileStatReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileStatReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['follows_count'] = self.follows_count
        context['frends_count'] = self.connect_count
        context['goods_count'] = self.goods_count
        context['communities_count'] = self.communities_count
        return context


def fixed(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_fixed=True
    item.save()
    return HttpResponse("!")


def unfixed(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_fixed=False
    item.save()
    return HttpResponse("!")

def item_delete(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_deleted=True
    item.save()
    return HttpResponse("!")
