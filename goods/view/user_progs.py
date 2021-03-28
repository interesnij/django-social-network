from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment, GoodSubCategory, GoodCategory, GoodAlbum
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from goods.forms import CommentForm, GoodForm, GoodAlbumForm
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform, get_detect_platform_template


class UserGoodAlbumAdd(View):
    def get(self,request,*args,**kwargs):
        list = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class UserGoodAlbumRemove(View):
    def get(self,request,*args,**kwargs):
        list = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


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
    template_name = "u_good/add.html"

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/u_good/add.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodUserCreate,self).get_context_data(**kwargs)
        context["form"] = GoodForm()
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        from common.processing.good import get_good_processing

        self.form, self.user = GoodForm(request.POST,request.FILES), User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid():
            from common.notify.notify import user_notify

            good = self.form.save(commit=False)
            albums = self.form.cleaned_data.get("album")
            images = request.POST.getlist('images')
            if not good.price:
                good.price = 0
            new_good = good.create_good(
                                        title=good.title,
                                        image=good.image,
                                        images=images,
                                        sub_category=GoodSubCategory.objects.get(pk=request.POST.get('sub_category')),
                                        creator=self.user,
                                        description=good.description,
                                        price=good.price,
                                        albums=albums,
                                        comments_enabled=good.comments_enabled,
                                        votes_on=good.votes_on,
                                        status="PG")
            get_good_processing(new_good)
            user_notify(request.user, new_post.creator.pk, None, "goo"+str(new_good.pk), "u_good_create", "ITE")
            return render_for_platform(request, 'goods/good_base/u_new_good.html',{'object': new_good})
        else:
            return HttpResponseBadRequest("")


class GoodAlbumUserCreate(TemplateView):
    """
    создание списка товаров пользователя
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/good_base/u_add_album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodAlbumUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(GoodAlbumUserCreate,self).get_context_data(**kwargs)
        context["form"] = GoodAlbumForm()
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

	def get(self,request,*args,**kwargs):
		self.album, self.template_name = GoodAlbum.objects.get(pk=self.kwargs["pk"]), get_settings_template("users/user_goods/album_preview.html", request.user, request.META['HTTP_USER_AGENT'])
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

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_settings_template("goods/good_base/u_edit_album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserGoodAlbumEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserGoodAlbumEdit,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["album"] = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.user, self.album = User.objects.get(pk=self.kwargs["pk"]), GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.form = GoodAlbumForm(request.POST,instance=self.album)
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            new_album = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserGoodAlbumEdit,self).get(request,*args,**kwargs)

class UserGoodAlbumDelete(View):
    def get(self,request,*args,**kwargs):
        user, album = User.objects.get(pk=self.kwargs["pk"]), GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user and album.type == GoodAlbum.ALBUM:
            album.is_deleted = True
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserGoodAlbumAbortDelete(View):
    def get(self,request,*args,**kwargs):
        user, album = User.objects.get(pk=self.kwargs["pk"]), GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user:
            album.is_deleted = False
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404
