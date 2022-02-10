from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment, GoodSubCategory, GoodCategory, GoodList
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from goods.forms import CommentForm, GoodForm
from django.http import Http404
from common.templates import get_settings_template, render_for_platform, get_detect_platform_template


class UserGoodDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserGoodRecover(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.restore_item()
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.comments_enabled = True
            good.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.comments_enabled = False
            good.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.votes_on = False
            good.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.votes_on = True
            good.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserUnHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.type = Good.PUBLISHED
            good.save(update_fields=['type'])
            return HttpResponse()
        else:
            raise Http404

class UserHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.type = Good.DRAFT
            good.save(update_fields=['type'])
            return HttpResponse()
        else:
            raise Http404

class GoodUserCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("goods/u_good/add.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodUserCreate,self).get_context_data(**kwargs)
        context["form"] = GoodForm()
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid():
            from common.notify.notify import user_notify

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
                                        community=None)
            return render_for_platform(request, 'goods/good_base/u_new_good.html',{'object': new_good})
        else:
            return HttpResponseBadRequest()

class GoodUserEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("goods/u_good/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodUserEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodUserEdit,self).get_context_data(**kwargs)
        context["form"] = GoodForm()
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["good"] = Good.objects.get(pk=self.kwargs["pk"])
        context["user"] = good.creator
        return context

    def post(self,request,*args,**kwargs):
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(request.POST,request.FILES, instance=self.good)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.good.pk:
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
            return render_for_platform(request, 'goods/good_base/u_new_good.html',{'object': new_good})
        else:
            return HttpResponseBadRequest()
