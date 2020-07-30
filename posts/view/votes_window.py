from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from posts.models import Post, PostComment
from communities.models import Community
from common.model.votes import PostVotes, PostCommentVotes
from rest_framework.exceptions import PermissionDenied
from common.template.post import get_permission_community_post, get_permission_user_post 


class PostUserLikeWindow(TemplateView):
    template_name="post_votes/u_like.html"

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = get_template_user_post(self.item.creator, "post_votes/", "page.html", request.user)
        return super(PostUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.item.window_likes()
        context["text"] = "Запись одобрили:"
        context["class_name"] = "u_all_posts_likes"
        return context

class PostUserDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = get_template_user_post(self.item.creator, "post_votes/", "page.html", request.user)
        return super(PostUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.item.window_dislikes()
        context["text"] = "Запись не одобрили:"
        context["class_name"] = "u_all_posts_dislikes"
        return context


class PostUserCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = get_template_user_post(self.comment.commenter, "post_votes/", "page.html", request.user)
        return super(PostUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Коммент одобрили:"
        context["class_name"] = "u_all_posts_comment_likes"
        return context


class PostUserCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = get_template_user_post(self.comment.commenter, "post_votes/", "page.html", request.user)
        return super(PostUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Коммент не одобрили:"
        context["class_name"] = "u_all_posts_comment_dislikes"
        return context

class PostCommunityLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = get_template_community_post(self.item.community, "post_votes/", "page.html", request.user)
        return super(PostCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.item.window_likes()
        context["text"] = "Запись одобрили:"
        context["class_name"] = "c_all_posts_likes"
        return context

class PostCommunityDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = get_template_community_post(self.item.community, "post_votes/", "page.html", request.user)
        return super(PostCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.item.window_dislikes()
        context["text"] = "Запись не одобрили:"
        context["class_name"] = "u_all_posts_dislikes"
        return context

class PostCommunityCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = get_template_community_post(self.comment.post.community, "post_votes/", "page.html", request.user)
        return super(PostCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Коммент одобрили:"
        context["class_name"] = "c_all_posts_comment_likes"
        return context

class PostCommunityCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = get_template_community_post(self.comment.post.community, "post_votes/", "page.html", request.user)
        return super(PostCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Коммент не одобрили:"
        context["class_name"] = "c_all_posts_comment_dislikes"
        return context


class AllPostUserLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = get_template_user_post(self.item.creator, "all_post_votes/", "page.html", request.user)
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
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = get_template_user_post(self.item.creator, "all_post_votes/", "page.html", request.user)
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
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = get_template_user_post(self.comment.commenter, "all_post_votes/", "page.html", request.user)
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
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = get_template_user_post(self.comment.commenter, "all_post_votes/", "page.html", request.user)
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
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')

        self.template_name = get_template_community_post(self.item.community, "all_post_votes/", "page.html", request.user)
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
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        self.template_name = get_template_community_post(self.item.community, "all_post_votes/", "page.html", request.user)
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
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = get_template_community_post(self.comment.post.community, "all_post_votes/", "page.html", request.user)
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
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = get_template_community_post(self.comment.post.community, "all_post_votes/", "page.html", request.user)
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
        self.template_name = get_template_community_post(self.item.community, "all_post_votes/", "page.html", request.user)
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
        self.template_name = get_template_user_post(self.item.creator, "all_post_votes/", "page.html", request.user)
        return super(AllPostUserRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostUserRepostWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Запись одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.item.get_reposts().values("user_id"))
        return users
