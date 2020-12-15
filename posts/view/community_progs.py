from django.views.generic.base import TemplateView
from users.models import User
from posts.models import *
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from communities.models import Community
from posts.forms import *
from common.attach.post_attacher import get_post_attach
from common.processing.post import get_post_processing, get_post_offer_processing
from common.check.community import check_can_get_lists, check_private_post_exists
from common.template.user import render_for_platform
from django.views.generic.base import TemplateView


class PostCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = PostForm(request.POST)
        community = Community.objects.get(pk=self.kwargs["pk"])

        check_private_post_exists(community)
        if (community.is_wall_close() or community.is_staff_post_member_can()) and not request.user.is_staff_of_community(community.pk):
            raise Http404
        elif (community.is_member_post_all_can() or community.is_member_post()) and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid():
            check_can_get_lists(request.user, community)
            post = form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('photo') or \
                request.POST.get('video') or request.POST.get('music') or \
                request.POST.get('good') or request.POST.get('article') or \
                request.POST.get('playlist') or request.POST.get('video_list') or \
                request.POST.get('photo_list') or request.POST.get('doc_list') or \
                request.POST.get('doc') or request.POST.get('user') or request.POST.get('community'):

                lists = request.POST.getlist("lists")
                new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=community, parent=None, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                return render_for_platform(request, 'posts/post_community/new_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostOfferCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = PostForm(request.POST)
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_private_post_exists(community)

        if community.is_wall_close():
            raise Http404
        elif community.is_staff_post_member_can() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid() and check_can_get_lists(request.user, community):
            check_can_get_lists(request.user, community)
            post = form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                lists = request.POST.getlist("lists")
                new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=community, parent=None, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                get_post_attach(request, new_post)
                get_post_offer_processing(new_post)
                return render_for_platform(request, 'posts/post_community/post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostCommunityCommentCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST, request.FILES)
        community = Community.objects.get(pk=request.POST.get('pk'))
        post = Post.objects.get(uuid=request.POST.get('uuid'))
        if not community.is_comment_post_send_all() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif community.is_comment_post_send_admin() and not request.user.is_staff_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid() and post.comments_enabled:
            check_can_get_lists(request.user,community)
            comment=form_post.save(commit=False)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                from common.attach.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, post=post, text=comment.text)
                get_comment_attach(request, new_comment, "item_comment")
                if request.user.pk != post.creator.pk:
                    new_comment.notification_community_comment(request.user, community)
                return render_for_platform(request, 'posts/c_post_comment/admin_parent.html',{'comment': new_comment, 'community': community})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()

class PostCommunityReplyCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST, request.FILES)
        community = Community.objects.get(pk=request.POST.get('pk'))
        parent = PostComment.objects.get(pk=request.POST.get('post_comment'))
        if not community.is_comment_post_send_all() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif community.is_comment_post_send_admin() and not request.user.is_staff_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid() and parent.post.comments_enabled:
            check_can_get_lists(request.user,community)
            comment=form_post.save(commit=False)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                from common.attach.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, text=comment.text, post=None)
                get_comment_attach(request, new_comment, "item_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_community_reply_comment(request.user, community)
                return render_for_platform(request, 'posts/c_post_comment/admin_reply.html',{'reply': new_comment, 'community': community, 'comment': parent})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.is_ajax() and (request.user.pk == comment.commenter.pk or request.user.is_staff_of_community(self.kwargs["pk"])):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.pk == comment.commenter.pk or request.user.is_staff_of_community(self.kwargs["pk"])):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostWallCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostWallCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityFixed(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(item.community.pk):
            item.is_fixed = True
            item.save(update_fields=['is_fixed'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityUnFixed(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(item.community.pk):
            item.is_fixed = False
            item.save(update_fields=['is_fixed'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityOffComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(item.community.pk):
            item.comments_enabled = False
            item.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityOnComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(item.community.pk):
            item.comments_enabled = True
            item.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(item.community.pk):
            item.is_deleted = True
            item.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostWallCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            item.is_deleted = True
            item.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostWallCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            item.is_deleted = False
            item.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(item.community.pk):
            item.is_deleted = False
            item.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(post.community.pk):
            post.votes_on = True
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(post.community.pk):
            post.votes_on = False
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Post.objects.get(uuid=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)


class CommunityPostListCreate(TemplateView):
    """
    создание списка записей сообщества
    """
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from common.template.community import get_community_manage_template

        self.c = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("posts/post_community/add_list.html", request.user, self.c.pk, request.META['HTTP_USER_AGENT'])
        return super(CommunityPostListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityPostListCreate,self).get_context_data(**kwargs)
        context["form"], context["community"] = PostListForm(), self.c
        return context

    def post(self,request,*args,**kwargs):
        self.form = PostListForm(request.POST)
        if request.is_ajax() and self.form.is_valid():
            from common.template.user import render_for_platform

            list = self.form.save(commit=False)
            list.creator = request.user
            list.community = self.c
            list.type = PostList.LIST
            list.save()
            return render_for_platform(request, 'communities/lenta/admin_list.html',{'list': list})
        else:
            return HttpResponse()
        return super(CommunityPostListCreate,self).get(request,*args,**kwargs)


class CommunityPostListEdit(TemplateView):
    """
    изменение списка записей сообщества
    """
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from common.template.community import get_community_manage_template

        self.c = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("posts/post_community/edit_list.html", request.user, self.c.pk, request.META['HTTP_USER_AGENT'])
        return super(CommunityPostListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityPostListEdit,self).get_context_data(**kwargs)
        context["list"] = PostList.objects.get(pk=self.kwargs["list_pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = PostList.objects.get(pk=self.kwargs["list_pk"])
        self.form = PostListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunityPostListEdit,self).get(request,*args,**kwargs)


class CommunityPostListDelete(View):
    def get(self,request,*args,**kwargs):
        list = PostList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.type == PostList.LIST and request.user.is_staff_of_community(self.kwargs["pk"]):
            list.type = PostList.DELETED
            list.save(update_fields=['type'])
            return HttpResponse()
        else:
            raise Http404

class CommunityPostListAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = PostList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            list.type = PostList.LIST
            list.save(update_fields=['type'])
            return HttpResponse()
        else:
            raise Http404
