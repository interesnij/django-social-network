
from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment, GoodSubCategory, GoodCategory, GoodAlbum
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from goods.forms import CommentForm, GoodForm, GoodAlbumForm
from rest_framework.exceptions import PermissionDenied
from common.processing.good import get_good_processing, get_good_offer_processing
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform, get_detect_platform_template


class GoodCommentUserCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        good = Good.objects.get(pk=request.POST.get("good_pk"))
        if not request.is_ajax() and not self.good.comments_enabled:
            raise Http404

        if request.is_ajax() and form_post.is_valid() and good.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.attach.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, good_comment=good, text=comment.text)
                get_comment_attach(request, new_comment, "good_comment")
                if request.user.pk != good.creator.pk:
                    new_comment.notification_user_comment(request.user)
                return render_for_platform(request, 'goods/u_good_comment/my_parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class GoodReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = GoodComment.objects.get(pk=request.POST.get('good_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.good_comment.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.attach.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, good_comment=None, text=comment.text)
                get_comment_attach(request, new_comment, "good_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_user_reply_comment(request.user)
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'goods/u_good_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class GoodCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class GoodCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserGoodDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.is_deleted = True
            good.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserGoodAbortDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and good.creator == request.user:
            good.is_deleted = False
            good.save(update_fields=['is_deleted'])
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
        good = Good.objects.get(uupk=self.kwargs["pk"])
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
    template_name = "u_good/add.html"
    form = None

    def get(self,request,*args,**kwargs):
        self.form = GoodForm()
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_detect_platform_template("goods/u_good/add.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodUserCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid():
            good = self.form.save(commit=False)
            albums = self.form.cleaned_data.get("album")
            new_good = good.create_good(
                title=good.title,
                image=good.image,
                sub_category=GoodSubCategory.objects.get(pk=request.POST.get('sub_category')),
                creator=self.user,
                description=good.description,
                price=good.price,
                comments_enabled=good.comments_enabled,
                votes_on=good.votes_on,
                status="PG")
            get_good_processing(new_good)
            for _album in albums:
                _album.good_album.add(new_good)
            return render_for_platform(request, 'goods/good_base/u_new_good.html',{'object': new_good})
        else:
            return HttpResponseBadRequest("")


class GoodAlbumUserCreate(TemplateView):
    """
    создание списка товаров пользователя
    """
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.form = GoodAlbumForm()
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_detect_platform_template("goods/good_base/u_add_album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodAlbumUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(GoodAlbumUserCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodAlbumForm(request.POST)
        if request.is_ajax() and self.form.is_valid():
            album = self.form.save(commit=False)
            new_album = GoodAlbum.objects.create(title=album.title, type=GoodAlbum.ALBUM, order=album.order, creator=request.user, community=None)
            return render_for_platform(request, 'users/user_goods_list/my_list.html',{'album': new_album})
        else:
            return HttpResponseBadRequest()
        return super(GoodAlbumUserCreate,self).get(request,*args,**kwargs)


class UserGoodAlbumPreview(TemplateView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.album = GoodAlbum.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("user_goods/album_preview.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserGoodAlbumPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserGoodAlbumPreview,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context


class UserGoodAlbumEdit(TemplateView):
    """
    изменение списка товаров пользователя
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("good_base/u_edit_album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserGoodAlbumEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserGoodAlbumEdit,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["album"] = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.form = GoodAlbumForm(request.POST,instance=self.album)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            album = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserGoodAlbumEdit,self).get(request,*args,**kwargs)

class UserGoodAlbumDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user and album.type == GoodAlbum.ALBUM:
            album.is_deleted = True
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserGoodAlbumAbortDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user:
            album.is_deleted = False
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404
