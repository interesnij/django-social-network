import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from goods.forms import GoodForm
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from stst.models import GoodNumbers


class UserGoods(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template_user(folder="u_good/", template="goods.html", request=request)
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
                        raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
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
                raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
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


class GoodUserCreate(TemplateView):
    template_name = "u_good/add.html"
    form = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(initial={"creator":self.user})
        return super(GoodUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from goods.models import GoodSubCategory, GoodCategory

        context = super(GoodUserCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid() and self.user.pk == request.user.pk:
            new_good = self.form.save(commit=False)
            new_good.creator = self.user
            new_good = self.form.save()
            html = render(request, 'good_base/new_good.html',{'object': new_good})
            return HttpResponse("")
        else:
            return HttpResponseBadRequest("")
        return super(GoodUserCreate,self).get(request,*args,**kwargs)


class GoodUserCreateAttach(TemplateView):
    template_name = "u_good/add_attach.html"
    form = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(initial={"creator":self.user})
        return super(GoodUserCreateAttach,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from goods.models import GoodSubCategory, GoodCategory

        context = super(GoodUserCreateAttach,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid():
            new_good = self.form.save(commit=False)
            new_good.creator = self.user
            new_good = self.form.save()
            html = render(request, 'u_good/good.html',{'object': new_good})
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
        return super(GoodUserCreateAttach,self).get(request,*args,**kwargs)
