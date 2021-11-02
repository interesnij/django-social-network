from django.views.generic.base import TemplateView
from goods.models import *
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.community import check_can_get_lists
from goods.forms import CommentForm, GoodForm, GoodListForm
from communities.models import Community
from common.templates import render_for_platform


class AddGoodListInCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["list_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.add_in_community_collections(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class RemoveGoodListFromCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["list_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_user_can_delete_list(community.pk):
            list.remove_in_community_collections(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


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


class GoodListCommunityCreate(TemplateView):
    """
    создание списка товаров сообщества
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_community_manage_template

        self.template_name = get_community_manage_template("goods/good_base/c_add_list.html", request.user, Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'])
        return super(GoodListCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(GoodListCommunityCreate,self).get_context_data(**kwargs)
        context["form"] = GoodListForm()
        context["community"] = Community.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodListForm(request.POST)
        self.c = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community(self.c.pk):
            list = self.form.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=self.c)
            return render_for_platform(request, 'communities/goods/main_list/admin_list.html',{'list': new_list, 'community': self.c})
        else:
            return HttpResponseBadRequest()
        return super(GoodListCommunityCreate,self).get(request,*args,**kwargs)


class CommunityGoodListEdit(TemplateView):
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_community_manage_template

        self.list = GoodList.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("goods/good_base/c_edit_list.html", request.user, self.list.community, request.META['HTTP_USER_AGENT'])
        return super(CommunityGoodListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGoodListEdit,self).get_context_data(**kwargs)
        context["list"] = GoodList.objects.get(pk=self.kwargs["pk"])
        context["community"] = list.community
        return context

    def post(self,request,*args,**kwargs):
        self.list = GoodList.objects.get(pk=self.kwargs["pk"])
        self.form = GoodListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community(self.list.community.pk):
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunityGoodListEdit,self).get(request,*args,**kwargs)

class CommunityGoodListDelete(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["pk"])
        c = list.community
        if request.is_ajax() and request.user.is_staff_of_community(c.pk) and list.type != GoodList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityGoodListRecover(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["pk"])
        c = list.community
        if request.is_ajax() and request.user.is_staff_of_community(c.pk):
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class GoodCommentCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        c = Community.objects.get(pk=request.POST.get('pk'))
        good = Good.objects.get(pk=request.POST.get("good_pk"))
        if request.is_ajax() and form_post.is_valid() and good.comments_enabled:
            comment=form_post.save(commit=False)

            check_can_get_lists(request.user, c)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, good=good, text=comment.text, community=c, sticker=request.POST.get('sticker'))
                return render_for_platform(request, 'goods/c_good_comment/parent.html',{'comment': new_comment, 'community': c})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class GoodReplyCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        c = Community.objects.get(pk=request.POST.get('pk'))
        parent = GoodComment.objects.get(pk=request.POST.get('good_comment'))

        if form_post.is_valid() and parent.good.comments_enabled:
            comment = form_post.save(commit=False)
            check_can_get_lists(request.user, c)

            if not c.is_comment_good_send_all() and not request.user.is_member_of_community(c.pk):
                raise Http404
            elif c.is_comment_good_send_admin() and not request.user.is_staff_of_community(c.pk):
                raise Http404
            elif request.is_ajax() and request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, good=parent.good, text=comment.text, community=c, sticker=request.POST.get('sticker'))
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'goods/c_good_comment/reply.html',{'reply': new_comment, 'comment': parent, 'community': c})
        else:
            return HttpResponseBadRequest()

class GoodCommunityCommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template

        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_my_template("generic/comment_edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodCommunityCommentEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommunityCommentEdit,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["form_post"] = CommentForm(instance=self.comment)
        context["btn_class"] = "c_good_edit_comment_btn"
        return context

    def post(self,request,*args,**kwargs):
        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        self.form = CommentForm(request.POST,instance=self.comment)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.comment.commenter.pk:
            from common.templates import render_for_platform
            _comment = self.form.save(commit=False)
            new_comment = _comment.edit_comment(text=_comment.text, attach = request.POST.getlist("attach_items"))
            if self.comment.parent:
                return render_for_platform(request, 'goods/c_good_comment/reply.html',{'reply': new_comment})
            else:
                return render_for_platform(request, 'goods/c_good_comment/parent.html',{'comment': new_comment})
        else:
            return HttpResponseBadRequest()

class GoodCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.good.community
        except:
            community = comment.parent.good.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404

class GoodCommentCommunityRecover(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.good.community
        except:
            community = comment.parent.good.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddGoodInCommunityList(View):
    def get(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        list = GoodList.objects.get(pk=self.kwargs["list_pk"])

        if request.is_ajax() and not list.is_item_in_list(good.pk) and request.user.is_administrator_of_community(list.community.pk):
            list.good_list.add(good)
            return HttpResponse()
        else:
            raise Http404

class RemoveGoodFromCommunityList(View):
    def get(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        list = GoodList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.is_item_in_list(good.pk) and request.user.is_administrator_of_community(list.community.pk):
            list.good_list.remove(good)
            return HttpResponse()
        else:
            raise Http404


class CommunityChangeGoodPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from communities.models import Community

        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator_of_community(community.pk):
            for item in json.loads(request.body):
                post = Good.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class CommunityChangeGoodListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from communities.model.list import CommunityGoodListPosition

        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator_of_community(community.pk):
            for item in json.loads(request.body):
                list = CommunityGoodListPosition.objects.get(list=item['key'], community=community.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()
