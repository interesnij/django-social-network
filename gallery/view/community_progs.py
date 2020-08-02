import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.community import check_can_get_lists
from django.shortcuts import render
from django.views.generic import ListView
from communities.models import Community
from rest_framework.exceptions import PermissionDenied
from common.template.photo import get_permission_community_photo
from django.http import Http404


class PhotoCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if not self.photo.comments_enabled:
            raise PermissionDenied('Комментарии для фотографии отключены')
        self.template_name = get_permission_community_photo(self.photo.community, "c_photo_comment/", "comments.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
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


class PhotoCommentCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        photo_comment = Photo.objects.get(uuid=request.POST.get('uuid'))

        if not community.is_comment_photo_send_all() and not request.user.is_member_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif community.is_comment_photo_send_admin() and not request.user.is_staff_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif request.is_ajax() and form_post.is_valid() and photo_comment.comments_enabled:
            comment=form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, photo_comment=photo_comment, text=comment.text)
                get_comment_attach(request, new_comment, "photo_comment")
                if request.user.pk != photo_comment.creator.pk:
                    new_comment.notification_community_comment(request.user, community)
                return render(request, 'c_photo_comment/admin_parent.html',{'comment': new_comment, 'community': community})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PhotoReplyCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        parent = PhotoComment.objects.get(pk=request.POST.get('photo_comment'))

        if not community.is_comment_photo_send_all() and not request.user.is_member_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif community.is_comment_photo_send_admin() and not request.user.is_staff_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif request.is_ajax() and form_post.is_valid() and parent.photo_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, photo_comment=None, text=comment.text)
                get_comment_attach(request, new_comment, "photo_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_community_reply_comment(request.user, community)
            else:
                return HttpResponseBadRequest()
            return render(request, 'c_photo_comment/admin_reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
        else:
            return HttpResponseBadRequest()

class PhotoCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent_comment.post.community
        if request.is_ajax() and request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PhotoCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent_comment.post.community
        if request.is_ajax() and request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")


class CommunityPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if request.is_ajax() and form_image.is_valid() and request.user.is_administrator_of_community_with_name(photo.community.name):
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        return super(CommunityPhotoDescription,self).post(request,*args,**kwargs)


class CommunityPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.is_deleted = True
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")

class CommunityPhotoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.is_deleted = False
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")


class CommunityOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class CommunityCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class CommunityOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
        return HttpResponse("!")

class CommunityOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
        return HttpResponse("!")

class CommunityOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.is_public = False
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")

class PhotoWallCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user or request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PhotoWallCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user or request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class CommunityOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.is_public = True
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")


class CommunityAddAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        try:
            album = Album.objects.get(community=community, title="Фото со страницы",  is_generic=True,)
        except:
            album = Album.objects.create(creator=request.user, community=community, title="Фото со страницы",  is_generic=True,)
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(community.name):
            photo.save(update_fields=['album'])
        return HttpResponse("!")

class CommunityRemoveAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community_with_name(community.name):
            photo.album = None
            try:
                album = Album.objects.get(community=community, title="Сохраненные фото",  is_generic=True,)
            except:
                return HttpResponse("!")
            photo.album = album
            photo.save()
        return HttpResponse("!")
