from django.views.generic.base import TemplateView
from users.models import User
from communities.models import Community
from main.forms import CommentForm
from django.views.generic import ListView
from generic.mixins import EmojiListMixin
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from main.models import Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied
from common.models import EmojiGroup, Emoji
from gallery.models import Photo, Album


class UserItemView(EmojiListMixin, TemplateView):
    model=Item
    template_name="lenta/user_item.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(uuid=self.kwargs["uuid"])
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.items = self.user.get_posts()
            self.item.views += 1
            self.item.save()
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif self.user == request.user and request.user.is_authenticated:
            self.items = self.user.get_posts()
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.items = self.user.get_posts()

        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()
        return super(UserItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserItemView,self).get_context_data(**kwargs)
        context["object"]=self.item
        context["user"]=self.user
        context["next"]=self.next
        context["prev"]=self.prev
        return context


class ItemListView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        emojies_1 = Emoji.objects.filter(group__order=1)
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user != self.request.user and self.request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=self.request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=self.request.user, user_id=self.user.id)
            items_list = self.user.get_posts().order_by('-created')
            current_page = Paginator(items_list, 10)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            items_list = self.user.get_posts().order_by('-created')
            current_page = Paginator(items_list, 12)
        elif self.user == request.user:
            items_list = self.user.get_posts().order_by('-created')
            current_page = Paginator(items_list, 12)

        context['emojies_1'] = emojies_1
        context['user'] = self.user
        page = request.GET.get('page')
        try:
            context['items_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['items_list'] = current_page.page(1)
        except EmptyPage:
            context['items_list'] = current_page.page(current_page.num_pages)

        return render_to_response('lenta/item_list.html', context)


class AllUsers(ListView):
    template_name="all_users.html"
    model=User

    def get_queryset(self):
        users=User.objects.only('id')
        return users


class ProfileUserView(TemplateView):
    template_name = 'user.html'
    is_blocked = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.avatar_album = Album.objects.get(creator=self.user, title="Фото со страницы", is_generic=True)
        self.avatar = Photo.objects.filter(album_2=self.avatar_album)[:1]
        try:
            self.is_frend = request.user.is_connected_with_user(self.user)
        except:
            self.is_frend = None
        if request.user.is_authenticated:
            self.is_blocked = request.user.has_blocked_user_with_id(self.user)
        self.communities=Community.objects.filter(memberships__user__id=self.user.pk)[0:5]
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['form_comment'] = CommentForm()
        context['communities'] = self.communities
        context['is_frend'] = self.is_frend
        context['is_blocked'] = self.is_blocked
        context['avatar'] = self.avatar
        return context
