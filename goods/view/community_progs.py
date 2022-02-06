from django.views.generic.base import TemplateView
from goods.models import *
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.community import check_can_get_lists
from goods.forms import CommentForm, GoodForm
from communities.models import Community
from common.templates import render_for_platform


class CommunityOpenCommentGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user or request.user.is_staff_of_community(good.community.pk):
            good.comments_enabled = True
            good.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityCloseCommentGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user or request.user.is_staff_of_community(good.community.pk):
            good.comments_enabled = False
            good.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user or request.user.is_staff_of_community(good.community.pk):
            good.votes_on = False
            good.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user or request.user.is_staff_of_community(good.community.pk):
            good.votes_on = True
            good.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404


class CommunityHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(good.community.pk):
            good.is_hide = True
            good.save(update_fields=['is_hide'])
            return HttpResponse()

class CommunityUnHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(good.community.pk):
            good.is_hide = False
            good.save(update_fields=['is_hide'])
            return HttpResponse()
        else:
            raise Http404

class CommunityGoodDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        c = good.community
        if request.is_ajax() and request.user.is_administrator_of_community(c.pk):
            good.delete_item(c)
            return HttpResponse()
        else:
            raise Http404

class CommunityGoodRecover(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        c = good.community
        if request.is_ajax() and request.user.is_staff_of_community(c.pk):
            good.restore_item(c)
            return HttpResponse()
        else:
            raise Http404


class GoodCommunityCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_community_manage_template
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("goods/c_good/add.html", request.user, self.community, request.META['HTTP_USER_AGENT'])
        return super(GoodCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommunityCreate,self).get_context_data(**kwargs)
        context["form"] = GoodForm()
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        if request.is_ajax() and self.form.is_valid():
            good = self.form.save(commit=False)
            new_good = good.create_good(
                                        title=good.title,
                                        image=good.image,
                                        images=request.POST.getlist('images'),
                                        list=good.list,
                                        sub_category=GoodSubCategory.objects.get(pk=request.POST.get('sub_category')),
                                        creator=request.user,
                                        description=good.description,
                                        price=good.price,
                                        comments_enabled=good.comments_enabled,
                                        votes_on=good.votes_on,
                                        community=good.community)
            return render_for_platform(request,'goods/good_base/c_new_good.html',{'object': new_good})
        else:
            return HttpResponseBadRequest()

class GoodCommunityEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.community = self.good.community
        self.template_name = get_community_manage_template("goods/c_good/edit.html", request.user, self.community, request.META['HTTP_USER_AGENT'])
        return super(GoodCommunityEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommunityEdit,self).get_context_data(**kwargs)
        context["form"] = GoodForm()
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["good"] = self.good
        context["community"] = self.good.community
        return context

    def post(self,request,*args,**kwargs):
        self.good = Good.objects.get(pk=self.kwargs["good_pk"])
        self.form = GoodForm(request.POST,request.FILES, instance=self.good)
        if request.is_ajax() and self.form.is_valid() and request.user.pk.is_administrator_of_community(self.kwargs["pk"]):
            from common.notify.notify import user_notify
            good = self.form.save(commit=False)
            new_good = self.good.edit_good(
                                        title=good.title,
                                        image=good.image,
                                        images=request.POST.getlist('images'),
                                        list=good.list,
                                        sub_category=GoodSubCategory.objects.get(pk=request.POST.get('sub_category')),
                                        description=good.description,
                                        price=good.price,
                                        comments_enabled=good.comments_enabled,
                                        votes_on=good.votes_on)
            return render_for_platform(request, 'goods/good_base/c_new_good.html',{'object': new_good})
        else:
            return HttpResponseBadRequest()
