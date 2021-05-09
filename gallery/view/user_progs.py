from users.models import User
from gallery.models import PhotoList, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm, PhotoListForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform
from django.views.generic.base import TemplateView


class AddPhotoListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemovePhotoListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
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
            photo = Photo.create_photo(creator=user, image=photo_input, list=_list, type="PHAVA")
            photo.list.add(_list)
            user.plus_photos(1)

            request.user.create_s_avatar(photo_input)
            request.user.create_b_avatar(photo_input)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserCreatePhotosInMainList(View):
    """
    асинхронная мульти загрузка фотографий пользователя в основной альбом
    """
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        photos = []
        if request.is_ajax() and self.user == request.user:
            list = PhotoList.objects.get(creator_id=self.user.id, community__isnull=True, type=PhotoList.MAIN)
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=self.user, image=p, list=list, type="PHO")
                photos += [photo,]
            self.user.plus_photos(len(photos))
            return render_for_platform(request, 'gallery/u_photo/new_photos.html', {'object_list': photos, 'user': request.user})
        else:
            raise Http404

class UserCreatePhotosInPhotoList(View):
    """
    асинхронная мульти загрузка фотографий пользователя в альбом
    """
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        photos = []
        uploaded_file = request.FILES['file']
        if request.is_ajax() and user == request.user:
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=user, image=p, list=list, type="PHLIS")
                photos += [photo,]
            user.plus_photos(len(photos))
            return render_for_platform(request, 'gallery/u_photo/new_list_photos.html',{'object_list': photos, 'list': _list, 'user': request.user})
        else:
            raise Http404

class PhotoAttachUserCreate(View):
    """
    мульти сохранение изображений с моментальным выводом в превью
    """
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photos = []
        if request.is_ajax() and user == request.user:
            try:
                list = PhotoList.objects.get(creator=request.user, community__isnull=True, type=PhotoList.WALL)
            except:
                list = PhotoList.objects.create(creator=request.user, type=PhotoList.WALL, name="Фото со стены", description="Фото со стены")
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=user, image=p, list=list, type="PHWAL")
                photos += [photo,]
            user.plus_photos(len(photos))
            return render_for_platform(request, 'gallery/u_photo/new_photos.html',{'object_list': photos, 'user': request.user})
        else:
            raise Http404


class PhotoCommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        photo = Photo.objects.get(uuid=request.POST.get('uuid'))

        if request.is_ajax() and form_post.is_valid() and photo.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, photo=photo, text=comment.text, community=None)
                return render_for_platform(request, 'gallery/u_photo_comment/my_parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PhotoReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = PhotoComment.objects.get(pk=request.POST.get('photo_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.photo_comment.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, photo=None, text=comment.text, community=None)
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'gallery/u_photo_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
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
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if request.is_ajax() and form_image.is_valid() and photo.creator.pk == request.user.pk:
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        else:
            raise Http404


class UserPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.delete_photo(None)
            return HttpResponse()
        else:
            raise Http404

class UserPhotoRecover(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.restore_photo(None)
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator.pk == request.user.pk:
            photo.make_private()
            return HttpResponse()
        else:
            raise Http404

class UserOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user:
            photo.make_publish()
            return HttpResponse()
        else:
            raise Http404

class PhotoWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == user.pk:
            comment.delete_comment()
            return HttpResponse()
        else:
            raise Http404

class PhotoWallCommentUserRecover(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == user.pk:
            comment.restore_comment()
            return HttpResponse()
        else:
            raise Http404


class UserRemoveAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
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
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=None,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'users/photos/list/new_list.html',{'list': new_list, 'user': self.user})
        else:
            return HttpResponseBadRequest()
        return super(PhotoListUserCreate,self).get(request,*args,**kwargs)

class PhotoListUserEdit(TemplateView):
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("users/photos/list/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoListUserEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoListUserEdit,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["user"] = self.user
        context["list"] = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        self.form = PhotoListForm(request.POST,instance=self.list)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            list = self.form.save(commit=False)
            new_list = list.edit_list(name=list.name, description=list.description, order=list.order, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(PhotoListUserEdit,self).get(request,*args,**kwargs)

class PhotoListUserDelete(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.creator.pk == request.user.pk and list.type == PhotoList.LIST:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class PhotoListUserRecover(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.restore_list()
            return HttpResponse()
        else:
            raise Http404


class AddPhotoInUserList(View):
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_item_in_list(photo.pk):
            list.photo_list.add(photo)
            return HttpResponse()
        else:
            raise Http404

class RemovePhotoFromUserList(View):
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(photo.pk):
            list.photo_list.remove(photo)
            return HttpResponse()
        else:
            raise Http404
