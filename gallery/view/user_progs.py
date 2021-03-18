from users.models import User
from gallery.models import Album, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm, AlbumForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform
from django.views.generic.base import TemplateView


class UserAlbumAdd(View):
    def get(self,request,*args,**kwargs):
        list = Album.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class UserAlbumRemove(View):
    def get(self,request,*args,**kwargs):
        list = Album.objects.get(uuid=self.kwargs["uuid"])
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
            from common.notify.notify import user_notify

            photo_input = request.FILES.get('file')
            try:
                _album = Album.objects.get(creator=user, type=Album.AVATAR, community__isnull=True)
            except:
                _album = Album.objects.create(creator=user, type=Album.AVATAR, title="Фото со страницы", description="Фото со страницы")
            photo = Photo.objects.create(file=photo_input, preview=photo_input,creator=user)
            photo.album.add(_album)

            request.user.create_s_avatar(photo_input)
            request.user.create_b_avatar(photo_input)
            user_notify(request.user, new_post.creator.pk, None, "pho"+str(photo.pk), "u_photo_create", "ITE")
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoUserCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя в основной альбом
    """
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        photos = []
        if request.is_ajax() and self.user == request.user:
            _album = Album.objects.get(creator_id=self.user.id, community__isnull=True, type=Album.MAIN)
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, preview=p, creator=self.user)
                _album.photo_album.add(photo)
                photos += [photo,]

            return render_for_platform(request, 'gallery/u_photo/new_photos.html', {'object_list': photos, 'user': request.user})
        else:
            raise Http404

class PhotoAlbumUserCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя в альбом
    """
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        _album = Album.objects.get(uuid=self.kwargs["uuid"])
        photos = []
        uploaded_file = request.FILES['file']
        if request.is_ajax() and user == request.user:
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, preview=p, creator=user)
                _album.photo_album.add(photo)
                photos += [photo,]
            return render_for_platform(request, 'gallery/u_photo/new_album_photos.html',{'object_list': photos, 'album': _album, 'user': request.user})
        else:
            raise Http404

class PhotoAttachUserCreate(View):
    """
    мульти сохранение изображений с моментальным выводом в превью
    """
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        photos = []
        if request.is_ajax() and self.user == request.user:
            try:
                _album = Album.objects.get(creator=request.user, community__isnull=True, type=Album.WALL)
            except:
                _album = Album.objects.create(creator=request.user, type=Album.WALL, title="Фото со стены", description="Фото со стены")
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, preview=p, creator=self.user)
                _album.photo_album.add(photo)
                photos += [photo,]
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
                from common.notify.notify import user_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, photo=photo, text=comment.text)
                user_notify(request.user, photo.creator.pk, None, "com"+str(new_comment.pk)+", pho"+str(photo.pk), "u_photo_comment_notify", "COM")
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
                from common.notify.notify import user_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, photo=None, text=comment.text)
                user_notify(request.user, parent.photo.creator.pk, None, "rep"+str(new_comment.pk)+",com"+str(parent.pk)+",pho"+str(parent.photo.pk), "u_photo_comment_notify", "REP")
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'gallery/u_photo_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class PhotoCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PhotoCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if request.is_ajax() and form_image.is_valid() and photo.creator.pk == request.user.pk:
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        else:
            raise Http404


class UserPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user:
            photo.is_deleted = True
            photo.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserPhotoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user:
            photo.is_deleted = False
            photo.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user:
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user:
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user:
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user:
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user:
            photo.is_public = False
            photo.save(update_fields=['is_public'])
            return HttpResponse()
        else:
            raise Http404

class UserOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user:
            photo.is_public = True
            photo.save(update_fields=['is_public'])
            return HttpResponse()
        else:
            raise Http404

class PhotoWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == user.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PhotoWallCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == user.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404


class UserRemoveAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user:
            photo.album = None
            album = Album.objects.get(creator=user, community__isnull=True, type=Album.AVATAR)
            photo.album = album
            photo.save()
            return HttpResponse()
        else:
            raise Http404


class UserAlbumPreview(TemplateView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.album = Album.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("users/user_album/album_preview.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserAlbumPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserAlbumPreview,self).get_context_data(**kwargs)
		context["album"], context["user"] = self.album, self.album.creator
		return context


class AlbumUserCreate(TemplateView):
    """
    создание альбома пользователя
    """
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.form = AlbumForm()
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("users/user_album/add_album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AlbumUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AlbumUserCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = AlbumForm(request.POST)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            album = self.form.save(commit=False)
            if not album.description:
                album.description = "Без описания"
            new_album = Album.objects.create(title=album.title, description=album.description, type=Album.ALBUM, is_public=album.is_public, order=album.order,creator=self.user)
            return render_for_platform(request, 'users/user_album/new_album.html',{'album': new_album, 'user': self.user})
        else:
            return HttpResponseBadRequest()
        return super(AlbumUserCreate,self).get(request,*args,**kwargs)

class AlbumUserEdit(TemplateView):
    """
    изменение альбома пользователя
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("users/user_album/edit_album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AlbumUserEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AlbumUserEdit,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["user"] = self.user
        context["album"] = Album.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.form = AlbumForm(request.POST,instance=self.album)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            album = self.form.save(commit=False)
            if not album.description:
                album.description = "Без описания"
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(AlbumUserEdit,self).get(request,*args,**kwargs)

class AlbumUserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user and album.type == Album.ALBUM:
            album.is_deleted = True
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class AlbumUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user:
            album.is_deleted = False
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404


class UserPhotoAlbumAdd(View):
    """
    Добавляем фото в любой альбом, если его там нет
    """
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        album = Album.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not album.is_photo_in_album(photo.pk):
            album.photo_album.add(photo)
            return HttpResponse()
        else:
            raise Http404

class UserPhotoAlbumRemove(View):
    """
    Удаляем фото из любого альбома, если он там есть
    """
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and album.is_photo_in_album(photo.pk):
            album.photo_album.remove(photo)
            return HttpResponse()
        else:
            raise Http404
