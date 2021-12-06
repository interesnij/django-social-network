from django.views.generic.base import TemplateView
from users.models import User
from posts.models import *
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from communities.models import Community
from posts.forms import *
from common.check.community import check_can_get_lists
from django.views.generic.base import TemplateView


class AddPostsListInCommunityCollections(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.add_in_community_collections(community)
        return HttpResponse()

class RemovePostsListFromCommunityCollections(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_delete_list(community.pk):
            list.remove_in_community_collections(community)
        return HttpResponse()


class PostCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = PostForm(request.POST)
        list = PostsList.objects.get(pk=self.kwargs["pk"])

        if (list.community and request.user.is_administrator_of_community(list.community.pk)) \
            or (not list.community and request.user.pk == list.creator.pk):
            can_create = True
        else:
            can_create = list.is_user_can_create_el(request.user.pk)

        if request.is_ajax() and form_post.is_valid() and can_create:
            post = form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.templates import render_for_platform

                attach = request.POST.getlist('attach_items')
                new_post = post.create_post(
                                            creator=request.user,
                                            attach=attach,
                                            text=post.text,
                                            category=post.category,
                                            list=list,
                                            parent=None,
                                            comments_enabled=post.comments_enabled,
                                            is_signature=post.is_signature,
                                            votes_on=post.votes_on,
                                            community=list.community
                                            )
                return render_for_platform(request, 'posts/post_community/admin_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()

class CommunitySaveCreatorDraftPost(View):
    def post(self,request,*args,**kwargs):
        from common.check.community import check_private_post_exists

        form_post = PostForm(request.POST)
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community

        check_private_post_exists(community)
        if request.is_ajax() and form_post.is_valid():
            check_can_get_lists(request.user, community)
            post = form_post.save(commit=False)
            new_post = post.create_creator_draft_post(
                                        creator=request.user,
                                        attach=request.POST.getlist('attach_items'),
                                        text=post.text,
                                        category=post.category,
                                        list=list,
                                        comments_enabled=post.comments_enabled,
                                        is_signature=post.is_signature,
                                        votes_on=post.votes_on,
                                        community=community
                                        )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunitySaveOfferDraftPost(View):
    def post(self,request,*args,**kwargs):
        from common.check.community import check_private_post_exists

        form_post = PostForm(request.POST)
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community

        check_private_post_exists(community)
        if request.is_ajax() and form_post.is_valid():
            check_can_get_lists(request.user, community)
            post = form_post.save(commit=False)
            new_post = post.create_creator_offer_post(
                                        creator=request.user,
                                        attach=request.POST.getlist('attach_items'),
                                        text=post.text,
                                        category=post.category,
                                        list=list,
                                        comments_enabled=post.comments_enabled,
                                        is_signature=post.is_signature,
                                        votes_on=post.votes_on,
                                        community=community
                                        )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class PostCommunityEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_admin_template
        self.post = Post.objects.get(pk=self.kwargs["pk"])
        self.community = self.post.community
        if request.user.is_administrator_of_community(self.community.pk):
            self.template_name = get_admin_template(self.community, "posts/post_community/edit_post.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PostCommunityEdit,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostCommunityEdit, self).get_context_data(**kwargs)
        context['post'] = self.post
        context['form'] = PostForm(instance=self.post)
        return context

    def post(self,request,*args,**kwargs):
        _post = Post.objects.get(pk=self.kwargs["pk"])
        community_pk = _post.community.pk
        form_post, attach = PostForm(request.POST, instance=_post), request.POST.getlist('attach_items')

        if request.is_ajax() and form_post.is_valid() and request.user.is_administrator_of_community(community_pk):
            post = form_post.save(commit=False)
            if post.text or attach:
                from common.templates import render_for_platform
                new_post = post.edit_post(text=post.text,category=post.category,list=post.list,attach=attach,comments_enabled=post.comments_enabled,is_signature=post.is_signature,votes_on=post.votes_on)
                return render_for_platform(request, 'posts/post_community/admin_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostCommunityCommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template

        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_my_template("generic/comment_edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostCommunityCommentEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityCommentEdit,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["form_post"] = CommentForm(instance=self.comment)
        context["btn_class"] = "c_post_edit_comment_btn"
        return context

    def post(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.form = CommentForm(request.POST,instance=self.comment)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.comment.commenter.pk:
            from common.templates import render_for_platform
            _comment = self.form.save(commit=False)
            new_comment = _comment.edit_comment(text=_comment.text, attach = request.POST.getlist("attach_items"))
            if self.comment.parent:
                return render_for_platform(request, 'posts/c_post_comment/reply.html',{'reply': new_comment})
            else:
                return render_for_platform(request, 'posts/c_post_comment/parent.html',{'comment': new_comment})
        else:
            return HttpResponseBadRequest()

class PostOfferCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        from common.check.community import check_private_post_exists

        form_post = PostForm(request.POST)
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community
        check_private_post_exists(community)

        if community.is_wall_close():
            raise Http404
        elif community.is_staff_post_member_can() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid():
            check_can_get_lists(request.user, community)
            post = form_post.save(commit=False)
            if request.POST.get('text') or request.POST.getlist('attach_items'):
                from common.notify.notify import community_notify
                from common.processing.post import get_post_offer_processing
                from common.templates import render_for_platform

                lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
                new_post = post.create_offer_post(
                                            creator=request.user,
                                            attach=attach,
                                            text=post.text,
                                            list=list,
                                            community=community)
                return render_for_platform(request, 'posts/post_community/post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostCommunityCommentCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST, request.FILES)
        community = Community.objects.get(pk=request.POST.get('pk'))
        post = Post.objects.get(post_pk=request.POST.get('pk'))
        if request.is_ajax() and form_post.is_valid() and post.comments_enabled:
            check_can_get_lists(request.user,community)
            comment=form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                from common.templates import render_for_platform
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, post=post, text=comment.text, community=community, sticker=request.POST.get('sticker'))
                return render_for_platform(request, 'posts/c_post_comment/parent.html',{'comment': new_comment, 'community': community})
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
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                from common.templates import render_for_platform
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, text=comment.text, post=parent.post, community=community, sticker=request.POST.get('sticker'))
                return render_for_platform(request, 'posts/c_post_comment/reply.html',{'reply': new_comment, 'community': community, 'comment': parent})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.is_ajax() and (request.user.pk == comment.commenter.pk or request.user.is_staff_of_community(self.kwargs["pk"])):
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404

class PostCommentCommunityRecover(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.pk == comment.commenter.pk or request.user.is_staff_of_community(self.kwargs["pk"])):
            comment.restore_item()
            return HttpResponse()
        else:
            raise Http404

class PostCommunityFixed(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(post.community.pk):
            post.fixed_community_post(post.community.pk)
            return HttpResponse()
        else:
            raise Http404

class PostCommunityUnFixed(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(post.community.pk):
            post.unfixed_community_post(post.community.pk)
            return HttpResponse()
        else:
            raise Http404

class PostCommunityOffComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(item.community.pk):
            item.comments_enabled = False
            item.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityOnComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(item.community.pk):
            item.comments_enabled = True
            item.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        c = post.community
        if request.is_ajax() and request.user.is_staff_of_community(c.pk):
            post.delete_item(c)
            return HttpResponse()
        else:
            raise Http404

class PostCommunityRecover(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        c = post.community
        if request.is_ajax() and request.user.is_staff_of_community(c.pk):
            post.restore_item(c)
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(post.community.pk):
            post.votes_on = True
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(post.community.pk):
            post.votes_on = False
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Post.objects.get(pk=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)


class CommunityPostsListCreate(TemplateView):
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from common.templates import get_community_manage_template
        self.c = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("posts/post_community/add_list.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
        return super(CommunityPostsListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CommunityPostsListCreate,self).get_context_data(**kwargs)
        c["form"], c["community"] = PostsListCreateForm(), self.c
        return c

    def post(self,request,*args,**kwargs):
        self.c = Community.objects.get(pk=self.kwargs["pk"])
        self.form = PostsListCreateForm(request.POST)
        if request.is_ajax() and self.form.is_valid():
            from common.templates import render_for_platform
            list = self.form.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=self.c)
            return render_for_platform(request, 'communities/lenta/admin_list.html',{'list': new_list})
        else:
            return HttpResponse()
        return super(CommunityPostsListCreate,self).get(request,*args,**kwargs)


class CommunityPostsListEdit(TemplateView):
    """
    изменение списка записей сообщества
    """
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from common.templates import get_community_manage_template

        self.list = PostsList.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("posts/post_community/edit_list.html", request.user, self.list.c, request.META['HTTP_USER_AGENT'])
        return super(CommunityPostsListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityPostsListEdit,self).get_context_data(**kwargs)
        context["list"] = self.list
        context["community"] = list.community
        return context

    def post(self,request,*args,**kwargs):
        self.list = PostsList.objects.get(pk=self.kwargs["pk"])
        self.form = PostsListEditForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community(self.list.c.pk):
            list = self.form.save(commit=False)
            new_list = list.edit_list(name=list.name, description=list.description)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunityPostsListEdit,self).get(request,*args,**kwargs)


class CommunityPostsListDelete(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.type != PostsList.MAIN and request.user.is_administrator_of_community(list.c.pk):
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityPostsListRecover(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddPostInCommunityList(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        list = PostsList.objects.get(pk=self.kwargs["list_pk"])

        if request.is_ajax() and not list.is_item_in_list(post.pk) and request.user.is_administrator_of_community(list.community.pk):
            list.post_list.add(post)
            return HttpResponse()
        else:
            raise Http404

class RemovePostFromCommunityList(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        list = PostsList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.is_item_in_list(post.pk) and request.user.is_administrator_of_community(list.community.pk):
            list.post_list.remove(post)
            return HttpResponse()
        else:
            raise Http404

class CommunityChangePostPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from communities.models import Community

        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator_of_community(community.pk):
            for item in json.loads(request.body):
                post = Post.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class CommunityChangePostsListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from communities.model.list import CommunityPostsListPosition

        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator_of_community(community.pk):
            for item in json.loads(request.body):
                list = CommunityPostsListPosition.objects.get(list=item['key'], community=community.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()
