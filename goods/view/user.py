import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good
from users.models import User
from common.check.user import check_user_can_get_list
from rest_framework.exceptions import PermissionDenied
from stst.models import GoodNumbers
from common.template.post import get_template_user_good, get_permission_user_good


class UserGoods(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])

        self.template_name = get_permission_user_good(self.photo.creator, "u_good/", "goods.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserGoods,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        if self.user.pk == self.request.user.pk:
            goods_list = self.user.get_my_goods().order_by('-created')
        else:
            goods_list = self.user.get_goods().order_by('-created')
        return goods_list


class UserGood(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        self.goods = self.user.get_goods()

        if request.user.is_authenticated:
            if self.user.pk == request.user.pk:
                self.template_name = "u_good/my_good.html"
                self.goods = self.user.get_my_goods()
            elif request.user.is_post_manager():
                self.template_name = "u_good/staff_good.html"
            elif self.user != request.user:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
                if self.user.is_closed_profile():
                    if  request.user.is_connected_with_user_with_id(user_id=self.user.pk) or request.user.is_followers_user_with_id(user_id=self.user.pk):
                        self.template_name = "u_good/good.html"
                    else:
                        self.template_name = "u_good/close_good.html"
                elif request.user.is_child() and not self.user.is_child_safety():
                    raise PermissionDenied('Это не проверенный профиль, поэтому может навредить ребенку.')
                else:
                    self.template_name = "u_good/good.html"
            try:
                GoodNumbers.objects.filter(user=request.user.pk, good=self.good.pk).exists()
            except:
                if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                    GoodNumbers.objects.create(user=request.user.pk, good=self.good.pk, platform=0)
                else:
                    GoodNumbers.objects.create(user=request.user.pk, good=self.good.pk, platform=1)
        elif request.user.is_anonymous:
            if self.user.is_closed_profile():
                self.template_name = "u_good/anon_close_good.html"
            elif not self.user.is_child_safety():
                raise PermissionDenied('Это не проверенный профиль, поэтому может навредить ребенку.')
            else:
                self.template_name = "u_good/anon_good.html"

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        self.next = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
        self.prev = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
        return super(UserGood,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserGood,self).get_context_data(**kwargs)
        context["object"] = self.good
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context


class GoodUserCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if not self.good.comments_enabled:
            raise PermissionDenied('Комментарии к товару отключены')

        self.template_name = get_permission_user_good(self.user, "u_good_comment/", "comments.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(GoodUserCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodUserCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.good
        context['user'] = self.user
        return context

    def get_queryset(self):
        comments = self.good.get_comments()
        return comments
