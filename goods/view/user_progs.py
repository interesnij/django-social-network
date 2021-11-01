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
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=None,is_public=request.POST.get("is_public"))
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
        context["user"] = self.request.user
        context["list"] = GoodList.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = GoodList.objects.get(pk=self.kwargs["pk"])
        self.form = GoodListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description, is_public=request.POST.get("is_public"))
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


class GoodCommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, user, good = CommentForm(request.POST), User.objects.get(pk=request.POST.get('pk')), Good.objects.get(pk=request.POST.get("good_pk"))
        if not request.is_ajax() and not self.good.comments_enabled:
            raise Http404

        if request.is_ajax() and form_post.is_valid() and good.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, good=good, text=comment.text, community=None, sticker=request.POST.get('sticker'))
                return render_for_platform(request, 'goods/u_good_comment/parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class GoodReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, user, parent = CommentForm(request.POST), User.objects.get(pk=request.POST.get('pk')), GoodComment.objects.get(pk=request.POST.get('good_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.good.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, good=parent.good, text=comment.text, community=None, sticker=request.POST.get('sticker'))
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'goods/u_good_comment/reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class GoodUserCommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template

        self.template_name = get_my_template("generic/comment_edit.html", request.user, request.META['HTTP_USER_AGENT'])
        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        return super(GoodUserCommentEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodUserCommentEdit,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["form_post"] = CommentForm(instance=self.comment)
        context["btn_class"] = "u_good_edit_comment_btn"
        return context

    def post(self,request,*args,**kwargs):
        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        self.form = CommentForm(request.POST,instance=self.comment)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.comment.commenter.pk:
            from common.templates import render_for_platform
            _comment = self.form.save(commit=False)
            new_comment = _comment.edit_comment(text=_comment.text, attach = request.POST.getlist("attach_items"))
            if self.comment.parent:
                return render_for_platform(request, 'goods/u_good_comment/reply.html',{'reply': new_comment})
            else:
                return render_for_platform(request, 'goods/u_good_comment/parent.html',{'comment': new_comment})
        else:
            return HttpResponseBadRequest()

class GoodCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404

class GoodCommentUserRecover(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddGoodInUserList(View):
    def get(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        list = GoodList.objects.get(pk=self.kwargs["list_pk"])

        if request.is_ajax() and not list.is_item_in_list(good.pk):
            list.good_list.add(good)
            return HttpResponse()
        else:
            raise Http404

class RemoveGoodFromUserList(View):
    def get(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        list = GoodList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.is_item_in_list(good.pk):
            list.good_list.remove(good)
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
