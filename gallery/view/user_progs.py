from users.models import User
from gallery.models import PhotoList, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm, PhotoListForm
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from common.templates import get_settings_template, render_for_platform
from django.views.generic.base import TemplateView


class AddPhotoListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.add_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemovePhotoListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class UserAddAvatar(View):
    """
    загрузка аватара пользователя
    """
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and user == request.user:
            photo_input = request.FILES.get('file')
            _list = PhotoList.objects.get(creator=user, type=PhotoList.AVATAR, community__isnull=True)
            photo = Photo.create_photo(creator=user, image=photo_input, list=_list, type="PHAVA", community=None)
            request.user.create_s_avatar(photo_input)
            request.user.create_b_avatar(photo_input)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoAttachUserCreate(View):
    def post(self, request, *args, **kwargs):
        photos = []
        if request.is_ajax():
            list = PhotoList.objects.get(creator=request.user, type="WAL", community=None)
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=request.user, image=p, list=list, type="PHWAL", community=None)
                photos += [photo,]
            return render_for_platform(request, 'gallery/u_photo/new_album_photos.html',{'object_list': photos, 'list': list})
        else:
            raise Http404


class PhotoCommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        photo = Photo.objects.get(pk=request.POST.get('photo_pk'))

        if request.is_ajax() and form_post.is_valid() and photo.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, photo=photo, text=comment.text, community=None, sticker=request.POST.get('sticker'))
                return render_for_platform(request, 'gallery/u_photo_comment/parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PhotoReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = PhotoComment.objects.get(pk=request.POST.get('photo_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.photo.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, photo=parent.photo, text=comment.text, community=None, sticker=request.POST.get('sticker'))
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'gallery/u_photo_comment/reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class PhotoUserCommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template

        self.template_name = get_my_template("generic/comment_edit.html", request.user, request.META['HTTP_USER_AGENT'])
        self.comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        return super(PhotoUserCommentEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoUserCommentEdit,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["form_post"] = CommentForm(instance=self.comment)
        context["btn_class"] = "u_photo_edit_comment_btn"
        return context

    def post(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        self.form = CommentForm(request.POST,instance=self.comment)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.comment.commenter.pk:
            from common.templates import render_for_platform
            _comment = self.form.save(commit=False)
            new_comment = _comment.edit_comment(text=_comment.text, attach = request.POST.getlist("attach_items"))
            if self.comment.parent:
                return render_for_platform(request, 'posts/u_photo_comment/reply.html',{'reply': new_comment})
            else:
                return render_for_platform(request, 'posts/u_photo_comment/parent.html',{'comment': new_comment})
        else:
            return HttpResponseBadRequest()

class PhotoCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.delete_comment()
            return HttpResponse()
        else:
            raise Http404

class PhotoCommentUserRecover(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.restore_comment()
            return HttpResponse()
        else:
            raise Http404

class UserPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if request.is_ajax() and form_image.is_valid() and photo.creator.pk == request.user.pk:
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        else:
            raise Http404


class UserPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserPhotoRecover(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.restore_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404


class UserRemoveAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        if request.is_ajax() and user.pk == request.user.pk:
            photo.list = None
            list = PhotoList.objects.get(creator=user, community__isnull=True, type=PhotoList.AVATAR)
            photo.list = list
            photo.save()
            return HttpResponse()
        else:
            raise Http404

class PhotoListUserCreate(TemplateView):
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("users/photos/list/add_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoListUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoListUserCreate,self).get_context_data(**kwargs)
        context["form"] = PhotoListForm()
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = PhotoListForm(request.POST)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
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
            return render_for_platform(request, 'users/photos/list/new_list.html',{'list': new_list, 'user': self.user})
        else:
            return HttpResponseBadRequest()
        return super(PhotoListUserCreate,self).get(request,*args,**kwargs)

class PhotoListUserEdit(TemplateView):
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("users/photos/list/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoListUserEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoListUserEdit,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["list"] = PhotoList.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = PhotoList.objects.get(pk=self.kwargs["pk"])
        self.form = PhotoListForm(request.POST,instance=self.list)
        self.user = self.list.creator
        if request.is_ajax() and self.form.is_valid() and self.list.creator.pk == request.user.pk and self.list.is_have_edit():
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
        return super(PhotoListUserEdit,self).get(request,*args,**kwargs)

class PhotoListUserDelete(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.creator.pk == request.user.pk and list.is_have_edit():
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class PhotoListUserRecover(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddPhotoInUserList(View):
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and not list.is_item_in_list(photo.pk):
            list.photo_list.add(photo)
            return HttpResponse()
        else:
            raise Http404

class RemovePhotoFromUserList(View):
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.is_item_in_list(photo.pk):
            list.photo_list.remove(photo)
            return HttpResponse()
        else:
            raise Http404

class UserChangePhotoPosition(View):
    def post(self,request,*args,**kwargs):
        import json

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                post = Photo.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class UserChangePhotoListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from users.model.list import UserPhotoListPosition

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                list = UserPhotoListPosition.objects.get(list=item['key'], user=user.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()
