import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good
from users.models import User
from common.check.user import check_user_can_get_list
from rest_framework.exceptions import PermissionDenied
from stst.models import GoodNumbers
from common.template.good import get_template_user_good, get_permission_user_good


class UserGoods(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])

        self.template_name = get_permission_user_good(self.user, "u_good/", "goods.html", request.user)
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
            if request.user.is_no_phone_verified():
                self.template_name = "main/phone_verification.html"
            elif self.user.pk == request.user.pk:
                if self.user.is_suspended():
                    self.template_name = "generic/u_template/you_suspended.html"
                elif self.user.is_blocked():
                    self.template_name = "generic/u_template/you_global_block.html"
                else:
                    self.template_name = "u_good/my_good.html"
            elif request.user.pk != self.user.pk:
                self.get_buttons_block = request.user.get_buttons_profile(self.user.pk)
                if self.user.is_suspended():
                    self.template_name = "generic/u_template/user_suspended.html"
                elif self.user.is_blocked():
                    self.template_name = "generic/u_template/user_global_block.html"
                elif request.user.is_user_manager() or request.user.is_superuser:
                    self.template_name = "u_good/staff_good.html"
                    self.get_buttons_block = request.user.get_staff_buttons_profile(self.user.pk)
                elif request.user.is_blocked_with_user_with_id(user_id=self.user.pk):
                    self.template_name = "generic/u_template/block_user.html"
                elif self.user.is_closed_profile():
                    if request.user.is_followers_user_with_id(user_id=self.user.pk) or request.user.is_connected_with_user_with_id(user_id=self.user.pk):
                        self.template_name = "u_good/good.html"
                    else:
                        self.template_name = "generic/u_template/close_user.html"
                elif request.user.is_child() and not self.user.is_child_safety():
                    self.template_name = "generic/u_template/no_child_safety.html"
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
            if user.is_suspended():
                template_name = "generic/u_template/anon_user_suspended.html"
            elif user.is_blocked():
                template_name = "generic/u_template/anon_user_global_block.html"
            elif user.is_closed_profile():
                template_name = "generic/u_template/anon_close_user.html"
            elif not user.is_child_safety():
                template_name = "generic/u_template/anon_no_child_safety.html"
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
        if not request.is_ajax() or not self.good.comments_enabled:
            raise Http404
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
