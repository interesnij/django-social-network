from django.views.generic.base import TemplateView
from users.models import User
from communities.models import Community
from django.views.generic import ListView
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from main.models import Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied


class UserItemView(TemplateView):
    model = Item
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.item.views += 1
        self.item.save()
        self.template_name = "lenta/user_item.html"

        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.items = self.user.get_posts()
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif self.user == request.user and request.user.is_authenticated:
            self.template_name = "lenta/my_item.html"
            self.items = self.user.get_posts()
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.items = self.user.get_posts()

        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()
        return super(UserItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserItemView,self).get_context_data(**kwargs)
        context["object"] = self.item
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context


class ItemListView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        template = None
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            items_list = self.user.get_posts().order_by('-created')
            template = 'lenta/item_list.html'
            current_page = Paginator(items_list, 10)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            items_list = self.user.get_posts().order_by('-created')
            template = 'lenta/item_list_anon.html'
            current_page = Paginator(items_list, 10)
        elif self.user == request.user:
            items_list = self.user.get_posts().order_by('-created')
            template = 'lenta/my_item_list.html'
            current_page = Paginator(items_list, 10)
        context['user'] = self.user
        context['request_user'] = request.user
        page = request.GET.get('page')
        try:
            context['items_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['items_list'] = current_page.page(1)
        except EmptyPage:
            context['items_list'] = current_page.page(current_page.num_pages)

        return render_to_response(template, context)

class AllUsers(TemplateView):
    template_name="all_users.html"

class AllUsersList(ListView):
    template_name="all_users_list.html"
    model=User
    paginate_by=2

    def get_queryset(self):
        users=User.objects.only('pk')
        return users


class AllCommonUsers(ListView):
    template_name="all_possible_users.html"
    model=User
    paginate_by=12

    def get_queryset(self):
        user=User.objects.get(pk=self.kwargs["pk"])
        if user.is_authenticated:
            common_list = user.get_possible_friends()
        return common_list

class ProfileUserView(TemplateView):
    template_name = None
    common_frends = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user == request.user:
            self.template_name = "account/my_user.html"
            self.online_frends = self.user.get_pop_online_connection()

        elif request.user != self.user and request.user.is_authenticated:
            if request.user.is_blocked_with_user_with_id(user_id=self.user.id):
                self.template_name = "account/request_user_block.html"
            elif self.user.is_closed_profile():
                if not request.user.is_connected_with_user_with_id(user_id=self.user.id):
                    self.template_name = "account/close_user.html"
                else:
                    self.template_name = "account/frend.html"
                    self.common_frends = self.user.get_common_friends_of_user(request.user)[0:5]
            else:
                self.template_name = "account/user.html"
                self.common_frends = self.user.get_common_friends_of_user(request.user)[0:5]

        elif request.user.is_anonymous and self.user.is_closed_profile():
            self.template_name = "account/close_user.html"

        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.template_name = "account/anon_open_user.html"

        self.online_frends = self.user.get_pop_online_connection()
        self.communities=Community.objects.filter(memberships__user__id=self.user.pk)[0:5]

        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['communities'] = self.communities
        context['common_frends'] = self.common_frends
        context['online_frends'] = self.online_frends
        return context
