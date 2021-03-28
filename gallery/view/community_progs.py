from gallery.models import Album, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm, AlbumForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.community import check_can_get_lists
from communities.models import Community
from common.template.user import render_for_platform
from common.template.community import get_community_manage_template
from django.http import Http404
from django.views.generic.base import TemplateView


class CommunityAlbumAdd(View):
    def post(self,request,*args,**kwargs):
        list = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.communities.add(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunityAlbumRemove(View):
    def post(self,request,*args,**kwargs):
        list = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_user_can_delete_list(community.pk):
            list.communities.remove(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class PhotoCommunityCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя в основной альбом
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            photos = []
            check_can_get_lists(request.user, community)
            _album = Album.objects.get(community=community, type=Album.MAIN)
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, preview=p, creator=request.user)
                _album.photo_album.add(photo)
                photos += [photo,]
            return render_for_platform(request, 'gallery/c_photo/new_photos.html',{'object_list': photos, 'community': community})
        else:
            raise Http404

class PhotoAlbumCommunityCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя в альбом
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        _album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            photos = []
            uploaded_file = request.FILES['file']
            check_can_get_lists(request.user, community)
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, preview=p, creator=request.user)
                _album.photo_album.add(photo)
                photos += [photo,]
            return render_for_platform(request, 'gallery/c_photo/new_album_photos.html',{'object_list': photos, 'album': _album, 'community': community})
        else:
            raise Http404

class PhotoAttachCommunityCreate(View):
    """
    мульти сохранение изображений с моментальным выводом в превью
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            photos = []
            check_can_get_lists(request.user, community)
            _album = Album.objects.filter(type=Album.WALL, community=community)[0]
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, preview=p, creator=request.user)
                _album.photo_album.add(photo)
                photos += [photo,]
            return render_for_platform(request, 'communities/gallery/list.html',{'object_list': photos, 'community': community})
        else:
            raise Http404


class CommunityAddAvatar(View):
    """
    загрузка аватара сообщества
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator_of_community(community.pk):
            from common.notify.notify import community_notify

            photo_input = request.FILES.get('file')
            try:
                _album = Album.objects.get(community=community, type=Album.AVATAR)
            except:
                _album = Album.objects.create(creator=community.creator, community=community, type=Album.AVATAR, description="Фото со страницы сообщества")
            photo = Photo.objects.create(file=photo_input, preview=photo_input, creator=request.user)
            photo.album.add(_album)
            community.create_s_avatar(photo_input)
            community.create_b_avatar(photo_input)
            community_notify(request.user, community, None, "pho"+str(photo.pk), "c_photo_notify", "ITE")
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class PhotoCommentCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        photo = Photo.objects.get(uuid=request.POST.get('uuid'))

        if not community.is_comment_photo_send_all() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif community.is_comment_photo_send_admin() and not request.user.is_staff_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid() and photo.comments_enabled:
            comment=form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.notify.notify import community_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, photo=photo, text=comment.text)
                community_notify(request.user, community, None, "phc"+str(new_comment.pk)+", pho"+str(photo.pk), "c_photo_comment_notify", "COM")
                return render_for_platform(request, 'gallery/c_photo_comment/admin_parent.html',{'comment': new_comment, 'community': community})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PhotoReplyCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        parent = PhotoComment.objects.get(pk=request.POST.get('photo_comment'))

        if not community.is_comment_photo_send_all() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif community.is_comment_photo_send_admin() and not request.user.is_staff_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid() and parent.photo_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.notify.notify import community_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parentt=parent, photo=None, text=comment.text)
                community_notify(request.user, community, None, "phr"+str(new_comment.pk)+",phc"+str(parent.pk)+",pho"+str(parent.photo.pk), "c_photo_comment_notify", "REP")
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'gallery/c_photo_comment/admin_reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
        else:
            return HttpResponseBadRequest()

class PhotoCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent.post.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PhotoCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent.post.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404


class CommunityPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if request.is_ajax() and form_image.is_valid() and request.user.is_administrator_of_community(community.pk):
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        else:
            raise Http404


class CommunityPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.delete_photo()
            return HttpResponse()
        else:
            raise Http404

class CommunityPhotoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.abort_delete_photo()
            return HttpResponse()
        else:
            raise Http404


class CommunityOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.is_public = False
            photo.save(update_fields=['is_public'])
            return HttpResponse()
        else:
            raise Http404

class PhotoWallCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user or request.user.is_staff_of_community(community.pk):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PhotoWallCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user or request.user.is_staff_of_community(community.pk):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.is_public = True
            photo.save(update_fields=['is_public'])
            return HttpResponse()
        else:
            raise Http404


class AlbumCommunityCreate(TemplateView):
    """
    создание альбома сообщества
    """
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("communities/album/add_album.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
        return super(AlbumCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AlbumCommunityCreate,self).get_context_data(**kwargs)
        context["form"] = AlbumForm()
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        self.form = AlbumForm(request.POST)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator_of_community(self.community.pk):
            album = self.form.save(commit=False)
            if not album.description:
                album.description = "Без описания"
            new_album = Album.objects.create(title=album.title, community=self.community, description=album.description, type=Album.ALBUM, is_public=album.is_public, order=album.order,creator=self.community.creator)
            return render_for_platform(request, 'communities/album/new_album.html',{'album': new_album, 'community': self.community})
        else:
            return HttpResponseBadRequest()
        return super(AlbumCommunityCreate,self).get(request,*args,**kwargs)

class AlbumCommunityEdit(TemplateView):
    """
    изменение альбома сообщества
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("communities/album/edit_album.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
        return super(AlbumCommunityEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AlbumCommunityEdit,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["community"] = self.community
        context["album"] = Album.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.form = AlbumForm(request.POST,instance=self.album)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community(self.community.pk):
            album = self.form.save(commit=False)
            if not album.description:
                album.description = "Без описания"
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(AlbumCommunityEdit,self).get(request,*args,**kwargs)

class AlbumCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(community.pk) and album.type == Album.ALBUM:
            album.is_deleted = True
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class AlbumCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(community.pk):
            album.is_deleted = False
            album.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404
