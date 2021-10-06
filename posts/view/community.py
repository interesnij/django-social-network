from django.views.generic.base import TemplateView
from django.views.generic import ListView
from communities.models import Community
from posts.models import Post, PostComment
from common.check.community import check_can_get_lists
from common.template.post import get_permission_community_post_2
from django.http import Http404


class PostCommunityCommentList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_comments

        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.community = self.post.community
        if not request.is_ajax() or not self.post.comments_enabled:
            raise Http404
        self.template_name = get_template_user_comments(self.post, "posts/c_post_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.post
        context['community'] = self.community
        return context

    def get_queryset(self):
        comments = self.post.get_comments()
        return comments


class PostCommunityDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_permission_community_post_2(Community.objects.get(uuid=self.kwargs["uuid"]), "posts/post_community/", "detail.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostCommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityDetail,self).get_context_data(**kwargs)
        context["object"] = self.object
        return context
