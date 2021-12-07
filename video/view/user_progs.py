from django.views.generic.base import TemplateView
from users.models import User
from video.models import Video, VideoComment, VideoList
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from django.views.generic import ListView
from video.forms import VideoListForm, VideoForm, CommentForm
from rest_framework.exceptions import PermissionDenied
from common.templates import get_settings_template, render_for_platform


class AddVideoListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.add_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemoveVideoListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class VideoCommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        video = Video.objects.get(pk=request.POST.get('video_pk'))

        if request.is_ajax() and form_post.is_valid() and video.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, video=video, text=comment.text, community=None, sticker=request.POST.get('sticker'))
                return render_for_platform(request, 'video/u_video_comment/parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class VideoReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = VideoComment.objects.get(pk=request.POST.get('video_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.video.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, video=parent.video, text=comment.text, community=None, sticker=request.POST.get('sticker'))
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'video/u_video_comment/reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class VideoUserCommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template

        self.template_name = get_my_template("generic/comment_edit.html", request.user, request.META['HTTP_USER_AGENT'])
        self.comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        return super(VideoUserCommentEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoUserCommentEdit,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["form_post"] = CommentForm(instance=self.comment)
        context["btn_class"] = "u_video_edit_comment_btn"
        return context

    def post(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        self.form = CommentForm(request.POST,instance=self.comment)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.comment.commenter.pk:
            from common.templates import render_for_platform
            _comment = self.form.save(commit=False)
            new_comment = _comment.edit_comment(text=_comment.text, attach = request.POST.getlist("attach_items"))
            if self.comment.parent:
                return render_for_platform(request, 'video/u_video_comment/reply.html',{'reply': new_comment})
            else:
                return render_for_platform(request, 'video/u_video_comment/parent.html',{'comment': new_comment})
        else:
            return HttpResponseBadRequest()

class VideoCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404

class VideoCommentUserRecover(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.restore_item()
            return HttpResponse()
        else:
            raise Http404

class UserVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserVideoRecover(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.restore_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.comments_enabled = True
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.comments_enabled = False
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.votes_on = False
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.votes_on = True
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.make_private()
            return HttpResponse()
        else:
            raise Http404

class UserOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.make_publish()
            return HttpResponse()
        else:
            raise Http404

class UserVideoCreate(TemplateView):
    template_name, form_post  = None, None
    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/user_create/create_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from video.models import VideoList
        from video.forms import VideoForm

        context = super(UserVideoCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        context['video_lists'] = VideoList.get_user_staff_lists(self.request.user.pk)
        return context

    def post(self,request,*args,**kwargs):
        from video.forms import VideoForm

        self.form_post = VideoForm(request.POST, request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form_post.is_valid():
            video = self.form_post.save(commit=False)
            new_video = video.create_video(creator=request.user,image=video.image, title=video.title,file=video.file,uri=video.uri,description=video.description,list=video.list,comments_enabled=video.comments_enabled,votes_on=video.votes_on,community=None)
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()

class UserVideoEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/user_create/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoEdit,self).get_context_data(**kwargs)
        context["form"] = VideoForm()
        context["sub_categories"] = VideoSubCategory.objects.only("id")
        context["categories"] = VideoCategory.objects.only("id")
        context["video"] = Video.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.video = Video.objects.get(pk=self.kwargs["pk"])
        self.form = VideoForm(request.POST,request.FILES, instance=self.video)

        if request.is_ajax() and self.form.is_valid() and request.user == self.user:
            video = self.form.save(commit=False)
            new_video = video.edit_video(
                                        title=new_video.title,
                                        file=new_video.file,
                                        uri=new_video.uri,
                                        description=new_video.description,
                                        list=new_video.list,
                                        comments_enabled=new_video.comments_enabled,
                                        votes_on=new_video.votes_on)
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()


class UserVideoListCreate(TemplateView):
    form_post = None
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/user_create/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoListCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoListForm()
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoListForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid():
            list = self.form_post.save(commit=False)
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
            return render_for_platform(request, 'users/video/list/my_list.html',{'list': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()

class UserVideolistEdit(TemplateView):
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/user_create/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideolistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideolistEdit,self).get_context_data(**kwargs)
        context["list"] = VideoList.objects.get(pk=self.kwargs["pk"])
        context["user"] = request.user
        return context

    def post(self,request,*args,**kwargs):
        if request.is_ajax() and self.form_post.is_valid():
            list = VideoListForm(request.POST,instance=self.list)
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

        return super(UserVideolistEdit,self).get(request,*args,**kwargs)

class UserVideolistDelete(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == list.creator.pk and list.type != VideoList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserVideolistRecover(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == list.creator.pk:
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddVideoInUserList(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        list = VideoList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and not list.is_item_in_list(video.pk):
            list.video_list.add(video)
            return HttpResponse()
        else:
            raise Http404

class RemoveVideoFromUserList(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        list = VideoList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.is_item_in_list(video.pk):
            list.video_list.remove(video)
            return HttpResponse()
        else:
            raise Http404


class UserChangeVideoPosition(View):
    def post(self,request,*args,**kwargs):
        import json

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                post = Video.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class UserChangeVideoListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from users.model.list import UserVideoListPosition

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                list = UserVideoListPosition.objects.get(list=item['key'], user=user.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()
