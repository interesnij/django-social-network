from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from goods.forms import GoodForm
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied


class UserGoods(ListView):
    template_name = None
    model = Good
    paginate_by = 30

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template_user(folder="good_user/", template="goods.html", request=request)
        return super(UserGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserGoods,self).get_context_data(**kwargs)
        context["user"]=self.user
        return context

    def get_queryset(self):
        goods_list = self.user.get_goods().order_by('-created')
        return goods_list


class UserGood(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.goods = self.user.get_goods()
        self.template_name = self.user.get_permission_list_user(folder="good_user/", template="good.html", request=request)
        self.next = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
        self.prev = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
        return super(UserGood,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserGood,self).get_context_data(**kwargs)
        context["object"] = self.good
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context


class GoodUserCreate(TemplateView):
    template_name="good_user/add.html"
    form=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.form=GoodForm(initial={"creator":self.user})
        return super(GoodUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from goods.models import GoodSubCategory, GoodCategory

        context=super(GoodUserCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        context["sub_categories"]=GoodSubCategory.objects.only("id")
        context["categories"]=GoodCategory.objects.only("id")
        context["user"]=self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form=GoodForm(request.POST,request.FILES)
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid():
            new_good=self.form.save(commit=False)
            new_good.creator=self.user
            new_good=self.form.save()
            html = render_to_response('good_user/good.html',{'object': new_good,'request': request})
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
        return super(GoodUserCreate,self).get(request,*args,**kwargs)


class GoodUserCreateAttach(TemplateView):
    template_name="good_user/add_attach.html"
    form=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.form=GoodForm(initial={"creator":self.user})
        return super(GoodUserCreateAttach,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from goods.models import GoodSubCategory, GoodCategory

        context=super(GoodUserCreateAttach,self).get_context_data(**kwargs)
        context["form"]=self.form
        context["sub_categories"]=GoodSubCategory.objects.only("id")
        context["categories"]=GoodCategory.objects.only("id")
        context["user"]=self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form=GoodForm(request.POST,request.FILES)
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid():
            new_good=self.form.save(commit=False)
            new_good.creator=self.user
            new_good=self.form.save()
            html = render_to_response('good_user/good.html',{'object': new_good,'request': request})
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
        return super(GoodUserCreateAttach,self).get(request,*args,**kwargs)
