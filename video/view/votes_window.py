from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from video.models import Video, VideoComment
from communities.models import Community
from common.model.votes import VideoVotes, VideoCommentVotes
from rest_framework.exceptions import PermissionDenied


class VideoUserLikeWindow(TemplateView):
    template_name="video_votes/u_like.html"

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if not self.video.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = self.video.creator.get_permission_list_user(folder="video_votes/", template="page.html", request=request)
        return super(VideoUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.video.window_likes()
        context["text"] = "Ролик одобрили:"
        context["class_name"] = "u_all_video_likes"
        return context

class VideoUserDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if not self.video.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = self.video.creator.get_permission_list_user(folder="video_votes/", template="page.html", request=request)
        return super(VideoUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.video.window_dislikes()
        context["text"] = "Ролик не одобрили:"
        context["class_name"] = "u_all_video_dislikes"
        return context


class VideoUserCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="video_votes/", template="page.html", request=request)
        return super(VideoUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Коммент одобрили:"
        context["class_name"] = "u_all_video_comment_likes"
        return context


class VideoUserCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="video_votes/", template="page.html", request=request)
        return super(VideoUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Коммент не одобрили:"
        context["class_name"] = "u_all_video_comment_dislikes"
        return context

class VideoCommunityLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if not self.video.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = self.Video.community.get_template_list(folder="video_votes/", template="page.html", request=request)
        return super(VideoCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.video.window_likes()
        context["text"] = "Ролик одобрили:"
        context["class_name"] = "c_all_video_likes"
        return context

class VideoCommunityDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if not self.video.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = self.video.community.get_template_list(folder="video_votes/", template="page.html", request=request)
        return super(VideoCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.video.window_dislikes()
        context["text"] = "Ролик не одобрили:"
        context["class_name"] = "u_all_video_dislikes"
        return context

class VideoCommunityCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.community.get_template_list(folder="video_votes/", template="page.html", request=request)
        return super(VideoCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Коммент одобрили:"
        context["class_name"] = "c_all_video_comment_likes"
        return context

class VideoCommunityCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.community.get_template_list(folder="video_votes/", template="page.html", request=request)
        return super(VideoCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Коммент не одобрили:"
        context["class_name"] = "c_all_video_comment_dislikes"
        return context


class AllVideoUserLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if not self.video.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = self.video.creator.get_permission_list_user(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoUserLikeWindow,self).get_context_data(**kwargs)
        context['video'] = self.video
        context['text'] = "Ролик одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.video.likes().values("user_id"))
        return users

class AllVideoUserDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if not self.video.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = self.video.creator.get_permission_list_user(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoUserDislikeWindow,self).get_context_data(**kwargs)
        context['video'] = self.video
        context['text'] = "Ролик не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.video.dislikes().values("user_id"))
        return users


class AllVideoUserCommentLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoUserCommentLikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.likes().values("user_id"))
        return users


class AllVideoUserCommentDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.dislikes().values("user_id"))
        return users


class AllVideoCommunityLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if not self.video.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = self.video.community.get_template_list(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoCommunityLikeWindow,self).get_context_data(**kwargs)
        context['video'] = self.video
        context['text'] = "Ролик одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.video.likes().values("user_id"))
        return users

class AllVideoCommunityDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if not self.video.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = self.video.community.get_template_list(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoCommunityDislikeWindow,self).get_context_data(**kwargs)
        context['video'] = self.video
        context['text'] = "Ролик не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.video.dislikes().values("user_id"))
        return users


class AllVideoommunityCommentLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.video.community.get_template_list(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.likes().values("user_id"))
        return users


class AllVideoCommunityCommentDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.video.community.get_template_list(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.dislikes().values("user_id"))
        return users


class AllVideoCommunityRepostWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.video.community.get_template_list(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoCommunityRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoCommunityRepostWindow,self).get_context_data(**kwargs)
        context['video'] = self.video
        context['text'] = "Роликом поделились:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.video.get_reposts().values("user_id"))
        return users

class AllVideoUserRepostWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.video.creator.get_permission_list_user(folder="all_video_votes/", template="page.html", request=request)
        return super(AllVideoUserRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllVideoUserRepostWindow,self).get_context_data(**kwargs)
        context['video'] = self.video
        context['text'] = "Ролик одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.video.get_reposts().values("user_id"))
        return users
