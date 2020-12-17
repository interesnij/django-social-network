from django.views.generic.base import TemplateView
from communities.models import Community
from gallery.models import Album, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from rest_framework.exceptions import PermissionDenied
from common.template.photo import get_template_community_photo, get_permission_community_photo
from common.check.community import check_can_get_lists
from django.http import Http404
from gallery.forms import PhotoDescriptionForm


class CommunityPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(community_id=self.community.pk, type=Album.MAIN)
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.community, "communities/gallery/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if request.user.is_authenticated and request.user.is_staff_of_community(self.community.pk):
            self.photo_list = self.album.get_staff_photos()
        else:
            self.photo_list = self.album.get_photos()
        return super(CommunityPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPhotosList,self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def get_queryset(self):
        photo_list = self.photo_list
        return photo_list

class CommunityAlbumPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.community, "communities/album/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if request.user.is_authenticated and request.user.is_staff_of_community(self.community.pk):
            self.photo_list = self.album.get_staff_photos()
        else:
            self.photo_list = self.album.get_photos()
        return super(CommunityAlbumPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAlbumPhotosList,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        return context

    def get_queryset(self):
        photo_list = self.photo_list
        return photo_list

class PhotoCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() or not self.photo.comments_enabled:
            raise Http404
        self.template_name = get_permission_community_photo(self.community, "gallery/c_photo_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhotoCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.photo
        context['community'] = self.community
        return context

    def get_queryset(self):
        check_can_get_lists(self.request.user, self.community)
        comments = self.photo.get_comments()
        return comments


class CommunityDetailAvatar(TemplateView):
    """
    страница отдельного фото альбома "Фото со страницы" сообщества с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        try:
            self.album = Album.objects.get(community=self.community, type=Album.AVATAR)
        except:
            self.album = Album.objects.create(creator=self.community.creator, community=self.community, type=Album.AVATAR, title="Фото со страницы", description="Фото со страницы")
        self.form_image = PhotoDescriptionForm(request.POST,instance=self.photo)
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.community, "gallery/c_photo/avatar/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.community
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["album"] = self.album
        return context

class CommunityFirstAvatar(TemplateView):
    """
    страница отдельного аватара сообщества с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        try:
            self.album = Album.objects.get(community=self.community, type=Album.AVATAR)
        except:
            self.album = Album.objects.create(creator=self.community.creator, community=self.community, type=Album.AVATAR, title="Фото со страницы", description="Фото со страницы")
        self.photo = self.album.get_first_photo()
        self.form_image = PhotoDescriptionForm(request.POST,instance=self.photo)
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.community, "gallery/c_photo/avatar/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityFirstAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityFirstAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.community
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["album"] = self.album
        return context


class CommunityPhoto(TemplateView):
    """
    страница фото, не имеющего альбома для сообщества с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.album.community, "gallery/c_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.album.community
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["album"] = self.album
        return context


class CommunityAlbumPhoto(TemplateView):
    """
    страница отдельного фото в альбоме для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.album.community, "gallery/c_photo/album_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if request.user.is_authenticated and request.user.is_administrator_of_community(self.album.community.pk):
            self.photos = self.album.get_staff_photos()
        else:
            self.photos = self.album.get_photos()
        return super(CommunityAlbumPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAlbumPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.album.community
        context["album"] = self.album
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class CommunityWallPhoto(TemplateView):
    """
    страница отдельного фото альбома сообщества "Фото со стены"
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.template.photo import get_permission_community_photo_detail

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        try:
            self.album = Album.objects.get(community=self.community, type=Album.WALL)
        except:
            self.album = Album.objects.create(creator=self.community.creator, community=self.community, type=Album.WALL, title="Фото со стены", description="Фото со стены")
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_community_photo_detail(self.community, self.photo, "gallery/c_photo/wall_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityWallPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityWallPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.community
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["album"] = self.album
        return context

class CommunityPostPhoto(TemplateView):
    """
    страница отдельного фото записи сообщества с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from posts.models import Post

        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.post.get_attach_photos()
        if request.is_ajax():
            self.template_name = get_permission_community_photo_detail(self.post.community, self.photo, "gallery/c_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityPostPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPostPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.post.community
        context["post"] = self.post
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context

class CommunityCommentPhoto(TemplateView):
    """
    страница отдельного фото комментария к записи сообщества с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from posts.models import PostComment

        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.photos = self.comment.get_attach_photos()
        if request.is_ajax():
            self.template_name = get_permission_community_photo_detail(self.post.community, self.photo, "gallery/c_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityCommentPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityCommentPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.post.community
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context

class GetCommunityPhoto(TemplateView):
    """
    страница отдельного фото. Для уведомлений и тому подобное
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            self.template_name = get_detect_platform_template("gallery/c_photo/photo/admin_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GetCommunityPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GetCommunityPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context
