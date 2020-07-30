import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list
from django.shortcuts import render
from users.models import User
from django.views.generic import ListView
from rest_framework.exceptions import PermissionDenied
from common.template.photo import get_permission_user_photo


class PhotoUserCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])

        self.template_name = get_permission_user_photo(self.photo.creator, "u_photo_comment/", "comments.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(PhotoUserCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhotoUserCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.photo
        context['user'] = self.user
        return context

    def get_queryset(self):
        comments = self.photo.get_comments()
        return comments


class PhotoCommentUserCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        photo_comment = Photo.objects.get(uuid=request.POST.get('uuid'))

        if form_post.is_valid() and photo_comment.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, photo_comment=photo_comment, text=comment.text)
                get_comment_attach(request, new_comment, "photo_comment")
                if request.user.pk != photo_comment.creator.pk:
                    new_comment.notification_user_comment(request.user)
                return render(request, 'u_photo_comment/my_parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PhotoReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = PhotoComment.objects.get(pk=request.POST.get('photo_comment'))

        if form_post.is_valid() and parent.photo_comment.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, photo_comment=None, text=comment.text)
                get_comment_attach(request, new_comment, "photo_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_user_reply_comment(request.user)
            else:
                return HttpResponseBadRequest()
            return render(request, 'u_photo_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class PhotoCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == comment.commenter.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PhotoCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == comment.commenter.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class UserPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if form_image.is_valid() and photo.creator.pk == request.user.pk:
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        return super(UserPhotoDescription,self).post(request,*args,**kwargs)


class UserPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.is_deleted = True
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")

class UserPhotoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.is_deleted = False
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")


class UserOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.is_public = False
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")

class UserOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.is_public = True
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")


class PhotoWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PhotoWallCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")


class UserAddAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        try:
            album = Album.objects.get(creator=user, community=None, title="Фото со страницы",  is_generic=True,)
        except:
            album = Album.objects.create(creator=user, community=None, title="Фото со страницы",  is_generic=True,)
        if user == request.user:
            photo.save(update_fields=['album'])
        return HttpResponse("!")

class UserRemoveAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.album = None
            try:
                album = Album.objects.get(creator=user, community=None, title="Сохраненные фото",  is_generic=True,)
            except:
                album = Album.objects.create(creator=user, community=None, title="Сохраненные фото",  is_generic=True,)
            photo.album = album
            photo.save()
        return HttpResponse("!")
