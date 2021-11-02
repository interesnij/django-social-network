from users.models import User
from posts.models import *
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View
from posts.forms import *
from django.http import Http404
from django.views.generic.base import TemplateView


class AddPostsListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        from common.check.user import check_user_can_get_list

        list = PostsList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.add_in_user_collections(request.user)
        return HttpResponse()

class RemovePostsListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        from common.check.user import check_user_can_get_list

        list = PostsList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
        return HttpResponse()


class PostUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, list, attach = PostForm(request.POST), PostsList.objects.get(pk=self.kwargs["pk"]), request.POST.getlist('attach_items')

        if request.is_ajax() and form_post.is_valid() and list.is_user_can_create_el(request.user.pk):
            post = form_post.save(commit=False)
            if post.text or attach:
                from common.templates import render_for_platform
                new_post = post.create_post(
                                            creator=request.user,
                                            text=post.text,
                                            category=post.category,
                                            list=list,
                                            attach=attach,
                                            parent=None,
                                            comments_enabled=post.comments_enabled,
                                            is_signature=post.is_signature,
                                            votes_on=post.votes_on,
                                            community=None
                                            )
                return render_for_platform(request, 'posts/post_user/my_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class UserSaveCreatorDraftPost(View):
    def post(self,request,*args,**kwargs):
        form_post, list = PostForm(request.POST), PostsList.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            new_post = post.create_creator_draft_post(
                                        creator=request.user,
                                        text=post.text,
                                        category=post.category,
                                        list=list,
                                        attach=request.POST.getlist('attach_items'),
                                        comments_enabled=post.comments_enabled,
                                        votes_on=post.votes_on,
                                        )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserSaveOfferDraftPost(View):
    def post(self,request,*args,**kwargs):
        form_post, list = PostForm(request.POST), PostsList.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            new_post = post.create_offer_draft_post(
                                        creator=request.user,
                                        text=post.text,
                                        category=post.category,
                                        list=list,
                                        attach=request.POST.getlist('attach_items'),
                                        comments_enabled=post.comments_enabled,
                                        votes_on=post.votes_on,
                                        )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class PostUserEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template
        self.post = Post.objects.get(pk=self.kwargs["pk"])
        if request.user.pk != self.post.creator.pk:
            raise Http404
        self.template_name = get_my_template("posts/post_user/edit_post.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostUserEdit,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostUserEdit, self).get_context_data(**kwargs)
        context['post'] = self.post
        context['form'] = PostForm(instance=self.post)
        return context

    def post(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        form_post, attach = PostForm(request.POST, instance=post), request.POST.getlist('attach_items')

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            if post.text or attach:
                from common.templates import render_for_platform
                new_post = post.edit_post(
                                            text=post.text,
                                            category=post.category,
                                            list=post.list,
                                            attach=attach,
                                            comments_enabled=post.comments_enabled,
                                            is_signature=post.is_signature,
                                            votes_on=post.votes_on,
                                            )
                return render_for_platform(request, 'posts/post_user/my_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostCommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, user, post = CommentForm(request.POST), User.objects.get(pk=request.POST.get('pk')), Post.objects.get(pk=request.POST.get('post_pk'))

        if request.is_ajax() and form_post.is_valid() and post.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user.pk != user.pk:
                from common.check.user import check_user_can_get_list

                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                from common.templates import render_for_platform

                new_comment = comment.create_comment(commenter=request.user, parent=None, community=None, attach=request.POST.getlist('attach_items'), post=post, text=comment.text, sticker=request.POST.get('sticker'))
                return render_for_platform(request, 'posts/u_post_comment/parent.html', {'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, user, parent = CommentForm(request.POST, request.FILES), User.objects.get(pk=request.POST.get('pk')), PostComment.objects.get(pk=request.POST.get('post_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.post.comments_enabled:
            comment=form_post.save(commit=False)
            if request.user != user:
                from common.check.user import check_user_can_get_list

                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
                from common.templates import render_for_platform

                new_comment = comment.create_comment(commenter=request.user, post=comment.get_item(), community=None, attach=request.POST.getlist('attach_items'), parent=parent, text=comment.text, sticker=request.POST.get('sticker'))
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'posts/u_post_comment/reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class PostUserCommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template

        self.template_name = get_my_template("generic/comment_edit.html", request.user, request.META['HTTP_USER_AGENT'])
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        return super(PostUserCommentEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostUserCommentEdit,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["form_post"] = CommentForm(instance=self.comment)
        context["btn_class"] = "u_post_edit_comment_btn"
        return context

    def post(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.form = CommentForm(request.POST,instance=self.comment)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.comment.commenter.pk:
            from common.templates import render_for_platform
            _comment = self.form.save(commit=False)
            new_comment = _comment.edit_comment(text=_comment.text, attach = request.POST.getlist("attach_items"))
            if self.comment.parent:
                return render_for_platform(request, 'posts/u_post_comment/reply.html',{'reply': new_comment})
            else:
                return render_for_platform(request, 'posts/u_post_comment/parent.html',{'comment': new_comment})
        else:
            return HttpResponseBadRequest()

class PostCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404

class PostCommentUserRecover(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.restore_item()
            return HttpResponse()
        else:
            raise Http404

class PostUserFixed(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user == post.creator:
            post.fixed_user_post(post.creator.pk)
            return HttpResponse()
        else:
            raise Http404

class PostUserUnFixed(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user == post.creator:
            post.unfixed_user_post(post.creator.pk)
            return HttpResponse()
        else:
            raise Http404


class PostUserOffComment(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user == post.creator and request.is_ajax():
            post.comments_enabled = False
            post.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostUserOnComment(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user == post.creator and request.is_ajax():
            post.comments_enabled = True
            post.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostUserDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == post.creator.pk:
            post.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class PostUserRecover(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == post.creator.pk:
            post.restore_item(None)
            return HttpResponse()
        else:
            raise Http404


class UserOnVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and post.creator == request.user:
            post.votes_on = True
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and post.creator == request.user:
            post.votes_on = False
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404


class PostGetVotes(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        data = {'like_count': post.likes_count(), 'dislike_count': post.dislikes_count()}
        return JsonResponse(data)


class UserPostsListCreate(TemplateView):
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.template_name = get_detect_platform_template("posts/post_user/add_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPostsListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPostsListCreate,self).get_context_data(**kwargs)
        context["form"] = PostsListForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form = PostsListForm(request.POST)
        if request.is_ajax() and self.form.is_valid():
            from common.templates import render_for_platform

            list = self.form.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=None)
            return render_for_platform(request, 'users/lenta/my_list.html',{'list': new_list})
        else:
            return HttpResponse()
        return super(UserPostsListCreate,self).get(request,*args,**kwargs)


class UserPostsListEdit(TemplateView):
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.template_name = get_detect_platform_template("posts/post_user/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPostsListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPostsListEdit,self).get_context_data(**kwargs)
        context["list"] = PostsList.objects.get(pk=self.kwargs["list_pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = PostsList.objects.get(pk=self.kwargs["list_pk"])
        self.form = PostsListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and self.list.creator.pk == request.user.pk:
            list = self.form.save(commit=False)
            new_list = list.edit_list(name=list.name, description=list.description)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPostsListEdit,self).get(request,*args,**kwargs)


class UserPostsListDelete(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.type != PostsList.MAIN and list.creator.pk == request.user.pk:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserPostsListRecover(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddPostInUserList(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        list = PostsList.objects.get(pk=self.kwargs["list_pk"])

        if request.is_ajax() and not list.is_item_in_list(post.pk):
            list.post_list.add(post)
            return HttpResponse()
        else:
            raise Http404

class RemovePostFromUserList(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        list = PostsList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.is_item_in_list(post.pk):
            list.post_list.remove(post)
            return HttpResponse()
        else:
            raise Http404


class UserChangePostPosition(View):
    def post(self,request,*args,**kwargs):
        import json

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                post = Post.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class UserChangePostsListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from users.model.list import UserPostsListPosition

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                list = UserPostsListPosition.objects.get(list=item['key'], user=user.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()
