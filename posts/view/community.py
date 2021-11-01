from django.views.generic.base import TemplateView
from django.views.generic import ListView
from communities.models import Community
from posts.models import Post, PostComment
from common.check.community import check_can_get_lists
from django.http import Http404


class PostCommunityDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_community_item, get_template_anon_community_item

        self.post = Post.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.post, "posts/post_community/", "detail.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.post, "posts/post_community/", "anon_detail.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostCommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityDetail,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context
