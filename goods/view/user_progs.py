from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment, GoodSubCategory, GoodCategory, GoodList
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from goods.forms import CommentForm, GoodForm, GoodListForm
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform, get_detect_platform_template


class AddGoodListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemoveGoodListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class UserGoodDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.delete_good()
            return HttpResponse()
        else:
            raise Http404

class UserGoodAbortDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.abort_delete_good()
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
            good.status = Good.STATUS_PUBLISHED
            good.save(update_fields=['status'])
            return HttpResponse()
        else:
            raise Http404

class UserHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.status = Good.STATUS_DRAFT
            good.save(update_fields=['status'])
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
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        if request.is_ajax() and self.form.is_valid():
            from common.notify.notify import user_notify

            good = self.form.save(commit=False)
            new_good = good.create_good(
                                        title=good.title,
                                        image=good.image,
                                        images=request.POST.getlist('images'),
                                        lists=request.POST.getlist('list'),
                                        sub_category=GoodSubCategory.objects.get(pk=request.POST.get('sub_category')),
                                        creator=request.user,
                                        description=good.description,
                                        price=good.price,
                                        comments_enabled=good.comments_enabled,
                                        votes_on=good.votes_on,
                                        community=None,
                                        is_public=request.POST.get("is_public"))
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
        return context

    def post(self,request,*args,**kwargs):
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(request.POST,request.FILES, instance=self.good)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.good.pk:
            from common.notify.notify import user_notify
            good = self.form.save(commit=False)
            new_good = self.good.create_good(
                                        title=good.title,
                                        image=good.image,
                                        images=request.POST.getlist('images'),
                                        lists=request.POST.getlist('list'),
                                        sub_category=GoodSubCategory.objects.get(pk=request.POST.get('sub_category')),
                                        description=good.description,
                                        price=good.price,
                                        comments_enabled=good.comments_enabled,
                                        votes_on=good.votes_on,
                                        is_public=request.POST.get("is_public"))
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
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=self.c,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'users/user_goods_list/my_list.html',{'list': new_list})
        else:
            return HttpResponseBadRequest()
        return super(GoodListUserCreate,self).get(request,*args,**kwargs)


class UserGoodListEdit(TemplateView):
    """
    изменение списка товаров пользователя
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_settings_template("goods/good_base/u_edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserGoodListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserGoodListEdit,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["list"] = GoodList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), GoodList.objects.get(uuid=self.kwargs["uuid"])
        self.form = GoodListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description, order=list.order, community=None,lists=request.POST.get("list"),is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserGoodListEdit,self).get(request,*args,**kwargs)

class UserGoodListDelete(View):
    def get(self,request,*args,**kwargs):
        user, list = User.objects.get(pk=self.kwargs["pk"]), GoodList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user and list.type == GoodList.LIST:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class UserGoodListAbortDelete(View):
    def get(self,request,*args,**kwargs):
        user, list = User.objects.get(pk=self.kwargs["pk"]), GoodList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user:
            list.abort_delete_list()
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
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.notify.notify import user_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, good=good, text=comment.text)
                user_notify(request.user, good.creator.pk, None, "goc"+str(new_comment.pk)+", goo"+str(good.pk), "u_good_comment_notify", "COM")
                return render_for_platform(request, 'goods/u_good_comment/my_parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class GoodReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, user, parent = CommentForm(request.POST), User.objects.get(pk=request.POST.get('pk')), GoodComment.objects.get(pk=request.POST.get('good_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.good_comment.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.notify.notify import user_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, good=None, text=comment.text)
                user_notify(request.user, parent.photo.creator.pk, None, "gor"+str(new_comment.pk)+",goc"+str(parent.pk)+",goo"+str(parent.good.pk), "u_good_comment_notify", "REP")
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'goods/u_good_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class GoodCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.delete_comment(self)
            return HttpResponse()
        else:
            raise Http404

class GoodCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.abort_delete_comment(self)
            return HttpResponse()
        else:
            raise Http404
