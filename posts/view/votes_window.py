from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from posts.models import Post, PostComment
from communities.models import Community
from common.model.votes import PostVotes, PostCommentVotes
from rest_framework.exceptions import PermissionDenied
from common.templates import get_template_user_item, get_template_anon_user_item, get_template_community_item, get_template_anon_community_item


class PostUserLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.item, "posts/post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.item, "posts/post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.item, "posts/post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.item, "posts/post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.comment.get_item(), "posts/post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.comment.get_item(), "posts/post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.comment.get_item(), "posts/post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.comment.get_item(), "posts/post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.item, "posts/post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.item, "posts/post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.item, "posts/post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.item, "posts/post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.comment.get_item(), "posts/post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.comment.get_item(), "posts/post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.comment.get_item(), "posts/post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.comment.get_item(), "posts/post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Коммент не одобрили:"
        context["class_name"] = "c_all_posts_comment_dislikes"
        return context


class AllPostUserLikeWindow(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.item, "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.item, "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.item, "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.item, "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.comment.get_item(), "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.comment.get_item(), "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.comment.get_item(), "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.comment.get_item(), "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')

        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.item, "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.item, "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if not self.item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.item, "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.item, "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.comment.get_item(), "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.comment.get_item(), "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.comment.get_item(), "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.comment.get_item(), "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.item, "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.item, "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.item, "posts/all_post_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.item, "posts/all_post_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllPostUserRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostUserRepostWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Запись одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.item.get_reposts().values("user_id"))
        return users
