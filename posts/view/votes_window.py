from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from posts.models import Post, PostComment
from communities.models import Community
from django.http import JsonResponse, HttpResponse
from common.model.votes import PostVotes, PostCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name
from rest_framework.exceptions import PermissionDenied


class PostUserLikeWindow(TemplateView):
    template_name="post_votes/u_like.html"

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.creator.get_permission_list_user(folder="post_votes/", template="page.html", request=request)
        return super(PostUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.item.window_likes()
        context["text"] = "Оценили:"
        return context

class PostUserDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.creator.get_permission_list_user(folder="post_votes/", template="page.html", request=request)
        return super(PostUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.item.window_dislikes()
        context["text"] = "Не оценили:"
        return context


class PostUserCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="post_votes/", template="page.html", request=request)
        return super(PostUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Оценили:"
        return context


class PostUserCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="post_votes/", template="page.html", request=request)
        return super(PostUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Не оценили:"
        return context

class PostCommunityLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.community.get_template_list(folder="post_votes/", template="page.html", request=request)
        return super(PostCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.item.window_likes()
        context["text"] = "Оценили:"
        return context

class PostCommunityDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.community.get_template_list(folder="post_votes/", template="page.html", request=request)
        return super(PostCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.item.window_dislikes()
        context["text"] = "Не оценили:"
        return context

class PostCommunityCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.community.get_template_list(folder="post_votes/", template="page.html", request=request)
        return super(PostCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Оценили:"
        return context

class PostCommunityCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.community.get_template_list(folder="post_votes/", template="page.html", request=request)
        return super(PostCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Не оценили:"
        return context

class AllPostUserLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.creator.get_permission_list_user(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostUserLikeWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Запись одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.item.likes().values("user_id"))
        return users

class AllPostUserDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.creator.get_permission_list_user(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostUserDislikeWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Запись не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.item.dislikes().values("user_id"))
        return users


class AllPostUserCommentLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostUserCommentLikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.likes().values("user_id"))
        return users


class AllPostUserCommentDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.dislikes().values("user_id"))
        return users


class AllPostCommunityLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.community.get_template_list(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostCommunityLikeWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Запись одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.item.likes().values("user_id"))
        return users

class AllPostCommunityDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.community.get_template_list(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostCommunityDislikeWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Запись не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.item.dislikes().values("user_id"))
        return users


class AllPostCommunityCommentLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.comment.post.community.get_template_list(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.likes().values("user_id"))
        return users


class AllPostCommunityCommentDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.comment.post.community.get_template_list(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.dislikes().values("user_id"))
        return users


class AllPostCommunityRepostWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.community.get_template_list(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostCommunityRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostCommunityRepostWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Записью поделились:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.item.get_reposts().values("user_id"))
        return users

class AllPostUserRepostWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.creator.get_permission_list_user(folder="all_post_votes/", template="page.html", request=request)
        return super(AllPostUserRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostUserRepostWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Запись одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.item.get_reposts().values("user_id"))
        return users
