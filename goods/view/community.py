import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good
from communities.models import Community
from django.http import HttpResponse, HttpResponseBadRequest
from goods.forms import GoodForm
from common.checkers import check_can_get_posts_for_community_with_name
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from stst.models import GoodNumbers


class CommunityGoods(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template(folder="c_good/", template="goods.html", request=request)
        return super(CommunityGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGoods,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        if self.request.user.is_staff_of_community_with_name(self.community.name):
            goods_list = self.user.get_admin_goods().order_by('-created')
        else:
            goods_list = self.user.get_goods().order_by('-created')
        return goods_list


class CommunityGood(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(uuid=self.kwargs["uuid"])
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.goods = self.user.get_goods()

        if request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_good/admin_good.html"
                self.goods = self.user.get_admin_goods()
            elif request.user.is_post_manager():
                self.template_name = "c_lenta/staff_good.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_lenta/good.html"
            else:
                self.template_name = "c_lenta/good.html"
            try:
                GoodNumbers.objects.filter(user=request.user.pk, good=self.good.pk).exists()
            except:
                if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                    GoodNumbers.objects.create(user=request.user.pk, good=self.good.pk, platform=0)
                else:
                    GoodNumbers.objects.create(user=request.user.pk, good=self.good.pk, platform=1)
        elif request.user.is_anonymous:
            if self.community.is_public():
                self.template_name = "c_lenta/anon_good.html"
            else:
                raise PermissionDenied('Ошибка доступа.')

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        self.next = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
        self.prev = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
        return super(CommunityGood,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGood,self).get_context_data(**kwargs)
        context["object"] = self.good
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context


class GoodCommunityCreate(TemplateView):
    template_name = "c_good/add.html"
    form = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(initial={"creator":request.user})
        return super(GoodCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from goods.models import GoodSubCategory, GoodCategory

        context = super(GoodCommunityCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid():
            new_good = self.form.save(commit=False)
            new_good.creator = self.user
            new_good = self.form.save()
            html = render(request,'good_base/new_good.html',{'object': new_good})
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
        return super(GoodCommunityCreate,self).get(request,*args,**kwargs)


class GoodCommunityCreateAttach(TemplateView):
    template_name = "c_good/add_attach.html"
    form = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(initial={"creator":request.user})
        return super(GoodCommunityCreateAttach,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from goods.models import GoodSubCategory, GoodCategory

        context = super(GoodCommunityCreateAttach,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid():
            new_good = self.form.save(commit=False)
            new_good.creator = request.user
            new_good = self.form.save()
            html = render(request, 'c_good/good.html',{'object': new_good})
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
        return super(GoodCommunityCreateAttach,self).get(request,*args,**kwargs)
