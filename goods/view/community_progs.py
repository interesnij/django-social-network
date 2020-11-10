
from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment, GoodAlbum
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.community import check_can_get_lists
from django.views.generic import ListView
from goods.forms import CommentForm, GoodForm, GoodAlbumForm
from communities.models import Community
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from common.processing.good import get_good_processing, get_good_offer_processing
from common.template.user import render_for_platform
from common.template.community import get_community_manage_template


class GoodCommentCommunityCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        good = Good.objects.get(pk=request.POST.get("good_pk"))
        if not request.is_ajax() and not self.good.comments_enabled:
            raise Http404
        if not community.is_comment_good_send_all() and not request.user.is_member_of_community(community.pk):
            raise PermissionDenied("Ошибка доступа.")
        elif community.is_comment_good_send_admin() and not request.user.is_staff_of_community(community.pk):
            raise PermissionDenied("Ошибка доступа.")
        elif request.is_ajax() and form_post.is_valid() and good.comments_enabled:
            comment=form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.attach.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, good_comment=good, text=comment.text)
                get_comment_attach(request, new_comment, "good_comment")
                if request.user.pk != good.creator.pk:
                    new_comment.notification_community_comment(request.user, community)
                return render_for_platform(request, 'goods/c_good_comment/admin_parent.html',{'comment': new_comment, 'community': community})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class GoodReplyCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        parent = GoodComment.objects.get(pk=request.POST.get('good_comment'))

        if form_post.is_valid() and parent.good_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_lists(request.user, community)

            if not community.is_comment_good_send_all() and not request.user.is_member_of_community(community.pk):
                raise PermissionDenied("Ошибка доступа.")
            elif community.is_comment_good_send_admin() and not request.user.is_staff_of_community(community.pk):
                raise PermissionDenied("Ошибка доступа.")
            elif request.is_ajax() and request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.attach.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, good_comment=None, text=comment.text)
                get_comment_attach(request, new_comment, "good_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_community_reply_comment(request.user, community)
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'goods/c_good_comment/admin_reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
        else:
            return HttpResponseBadRequest()

class GoodCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.good.community
        except:
            community = comment.parent_comment.good.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class GoodCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.good.community
        except:
            community = comment.parent_comment.good.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404


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
        if request.is_ajax() and good.creator == request.user or request.user.is_staff_of_community(good.community.pk):
            good.is_hide = True
            good.save(update_fields=['is_hide'])
            return HttpResponse("!")

class CommunityUnHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user or request.user.is_staff_of_community(good.community.pk):
            good.is_hide = False
            good.save(update_fields=['is_hide'])
            return HttpResponse()
        else:
            raise Http404

class CommunityGoodDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user or request.user.is_staff_of_community(good.community.pk):
            good.is_delete = True
            good.save(update_fields=['is_delete'])
            return HttpResponse()
        else:
            raise Http404

class CommunityGoodAbortDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user or request.user.is_staff_of_community(good.community.pk):
            good.is_delete = False
            good.save(update_fields=['is_delete'])
            return HttpResponse()
        else:
            raise Http404


class GoodCommunityCreate(TemplateView):
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(initial={"creator":request.user})
        self.template_name = get_community_manage_template("good/c_good/add.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
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
        if request.is_ajax() and self.form.is_valid():
            new_good = self.form.save(commit=False)
            albums = self.form.cleaned_data.get("album")
            new_good.creator = request.user
            new_good = self.form.save()
            get_good_processing(new_good)
            for _album in albums:
                _album.good_album.add(new_good)
            return render_for_platform(request,'goods/good_base/c_new_good.html',{'object': new_good})
        else:
            return HttpResponseBadRequest()


class GoodAlbumCommunityCreate(TemplateView):
    """
    создание списка товаров сообщества
    """
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.form = GoodAlbumForm()
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("good/good_base/c_add_album.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
        return super(GoodAlbumCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(GoodAlbumCommunityCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodAlbumForm(request.POST)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community(self.community.pk):
            album = self.form.save(commit=False)
            new_album = GoodAlbum.objects.create(title=album.title, type=GoodAlbum.ALBUM, order=album.order, creator=request.user, community=self.community)
            return render_for_platform(request, 'goods/c_goods_list/admin_list.html',{'album': new_album, 'community': self.community})
        else:
            return HttpResponseBadRequest()
        return super(GoodAlbumCommunityCreate,self).get(request,*args,**kwargs)


class CommunityGoodAlbumEdit(TemplateView):
    """
    изменение списка товаров пользователя
    """
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("good/good_base/c_edit_album.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
        return super(CommunityGoodAlbumEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGoodAlbumEdit,self).get_context_data(**kwargs)
        context["community"] = self.community
        context["album"] = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.form = GoodAlbumForm(request.POST,instance=self.album)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community(self.community.pk):
            album = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunityGoodAlbumEdit,self).get(request,*args,**kwargs)

class CommunityGoodAlbumDelete(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk) and album.type == GoodAlbum.ALBUM:
            album.is_deleted = True
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class CommunityGoodAlbumAbortDelete(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            album.is_deleted = False
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404
