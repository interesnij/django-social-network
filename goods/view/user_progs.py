from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment, GoodSubCategory, GoodCategory, GoodList
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from goods.forms import CommentForm, GoodForm, GoodListForm
from django.http import Http404
from common.templates import get_settings_template, render_for_platform, get_detect_platform_template


class AddGoodListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.add_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemoveGoodListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class UserGoodDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserGoodRecover(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.restore_item()
            return HttpResponse(None)
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


class GoodListUserCreate(TemplateView):
    """
    создание списка товаров пользователя
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/good_base/u_add_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodListUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(GoodListUserCreate,self).get_context_data(**kwargs)
        context["form"] = GoodListForm()
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodListForm(request.POST)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            new_list = list.create_list(
                creator=request.user,
                name=list.name,
                description=list.description,
                community=None,
                can_see_el=list.can_see_el,
                can_see_el_users=request.POST.getlist("can_see_el_users"),
                can_see_comment=list.can_see_comment,
                can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                create_el=list.create_el,
                create_el_users=request.POST.getlist("create_el_users"),
                create_comment=list.create_comment,
                create_comment_users=request.POST.getlist("create_comment_users"),
                copy_el=list.copy_el,
                copy_el_users=request.POST.getlist("create_copy_el"),)
            return render_for_platform(request, 'users/goods/main_list/my_list.html',{'list': new_list})
        else:
            return HttpResponseBadRequest()
        return super(GoodListUserCreate,self).get(request,*args,**kwargs)


class UserGoodListEdit(TemplateView):
    """
    изменение списка товаров пользователя
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("goods/good_base/u_edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserGoodListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserGoodListEdit,self).get_context_data(**kwargs)
        context["list"] = GoodList.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = GoodList.objects.get(pk=self.kwargs["pk"])
        self.form = GoodListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            new_list = list.edit_list(
                name=list.name,
                description=list.description,
                can_see_el=list.can_see_el,
                can_see_el_users=request.POST.getlist("can_see_el_users"),
                can_see_comment=list.can_see_comment,
                can_see_comment_users=request.POST.getlist("can_see_comment_users"),
                create_el=list.create_el,
                create_el_users=request.POST.getlist("create_el_users"),
                create_comment=list.create_comment,
                create_comment_users=request.POST.getlist("create_comment_users"),
                copy_el=list.copy_el,
                copy_el_users=request.POST.getlist("copy_el_users"),)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserGoodListEdit,self).get(request,*args,**kwargs)

class UserGoodListDelete(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == list.creator.pk and list.type != GoodList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserGoodListRecover(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == list.creator.pk:
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404

class UserChangeGoodPosition(View):
    def post(self,request,*args,**kwargs):
        import json

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                post = Good.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class UserChangeGoodListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from users.model.list import UserGoodListPosition

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                list = UserGoodListPosition.objects.get(list=item['key'], user=user.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()
