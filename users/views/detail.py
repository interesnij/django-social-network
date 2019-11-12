from django.views.generic.base import TemplateView
from users.models import User
from communities.models import Community
from main.forms import CommentForm
from django.views.generic import ListView
from generic.mixins import EmojiListMixin
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from users.forms import AvatarUserForm
from main.models import Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.shortcuts import render_to_response


class UserItemView(EmojiListMixin, TemplateView):
    model=Item
    template_name="lenta/user_item.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
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


class ItemListView(View, EmojiListMixin):

    def get(self, request, **kwargs):
        context = {}
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile: 
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
        item_list = self.user.get_posts().order_by('-created')
        current_page = Paginator(item_list, 10)
        page = request.GET.get('page')
        context['user'] = self.user
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
