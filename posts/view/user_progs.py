from users.models import User
from posts.models import *
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View
from posts.forms import *
from django.http import Http404
from django.views.generic.base import TemplateView


class AddPostListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = PostList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemovePostListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = PostList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class PostUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, list, attach = PostForm(request.POST), request.POST.get("lists"), request.POST.getlist('attach_items')

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            if post.text or attach:
                from common.template.user import render_for_platform
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
                                            is_public=request.POST.get("is_public"),
                                            community=None
                                            )
                return render_for_platform(request, 'posts/post_user/new_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class UserPostView(View):
    def get(self,request,*args,**kwargs):
        from stst.models import PostNumbers

        if request.is_ajax() and request.user.is_authenticated:
            try:
                post = Post.objects.get(uuid=self.kwargs["uuid"])
            except:
                pass
            if PostNumbers.objects.filter(user=request.user.pk, post=post.pk).exists():
                pass
            else:
                PostNumbers.objects.create(user=request.user.pk, post=post.pk, device=request.user.get_device())
                post.plus_views(1)
        else:
            pass
        return HttpResponse()

class UserAdPostView(View):
    def get(self,request,*args,**kwargs):
        from stst.models import PostAdNumbers

        if request.is_ajax() and request.user.is_authenticated:
            post = Post.objects.get(uuid=self.kwargs["uuid"])
            if PostNumbers.objects.filter(user=request.user.pk, post=post.pk).exists():
                pass
            else:
                PostAdNumbers.objects.get(user=request.user.pk, post=post.pk, device=request.user.get_device())
                post.plus_ad_views(1)
            return HttpResponse()
        else:
            raise Http404


class PostCommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, user, post = CommentForm(request.POST), User.objects.get(pk=request.POST.get('pk')), Post.objects.get(uuid=request.POST.get('uuid'))

        if request.is_ajax() and form_post.is_valid() and post.comments_enabled:
            from common.check.user import check_user_can_get_list

            comment = form_post.save(commit=False)

            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.template.user import render_for_platform

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, post=post, text=comment.text, community=None)
                return render_for_platform(request, 'posts/u_post_comment/my_parent.html', {'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, user, parent = CommentForm(request.POST, request.FILES), User.objects.get(pk=request.POST.get('pk')), PostComment.objects.get(pk=request.POST.get('post_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.post.comments_enabled:
            from common.check.user import check_user_can_get_list

            comment=form_post.save(commit=False)
            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.template.user import render_for_platform

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, post=parent.post, text=comment.text, community=None)
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'posts/u_post_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
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

class PostWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.is_ajax() and request.user.pk == int(self.kwargs["pk"]):
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404

class PostWallCommentUserRecover(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.is_ajax() and request.user.pk == int(self.kwargs["pk"]):
            comment.restore_item()
            return HttpResponse()
        else:
            raise Http404

class PostUserFixed(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user == post.creator:
            post.fixed_user_post(post.creator.pk)
            return HttpResponse()
        else:
            raise Http404

class PostUserUnFixed(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user == post.creator:
            post.unfixed_user_post(post.creator.pk)
            return HttpResponse()
        else:
            raise Http404


class PostUserOffComment(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user == post.creator and request.is_ajax():
            post.comments_enabled = False
            post.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostUserOnComment(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user == post.creator and request.is_ajax():
            post.comments_enabled = True
            post.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostUserDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == post.creator.pk:
            post.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class PostWallUserDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == int(self.kwargs["pk"]):
            post.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class PostUserRecover(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == post.creator.pk:
            post.restore_item(None)
            return HttpResponse()
        else:
            raise Http404

class PostWallUserRecover(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == int(self.kwargs["pk"]):
            post.restore_item(None)
            return HttpResponse()
        else:
            raise Http404


class UserOnVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and post.creator == request.user:
            post.votes_on = True
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and post.creator == request.user:
            post.votes_on = False
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404


class PostGetVotes(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        data = {'like_count': post.likes_count(), 'dislike_count': post.dislikes_count()}
        return JsonResponse(data)


class UserPostListCreate(TemplateView):
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from common.template.user import get_detect_platform_template

        self.template_name = get_detect_platform_template("posts/post_user/add_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPostListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPostListCreate,self).get_context_data(**kwargs)
        context["form"] = PostListForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form = PostListForm(request.POST)
        if request.is_ajax() and self.form.is_valid():
            from common.template.user import render_for_platform

            list = self.form.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=None,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'users/lenta/my_list.html',{'list': new_list})
        else:
            return HttpResponse()
        return super(UserPostListCreate,self).get(request,*args,**kwargs)


class UserPostListEdit(TemplateView):
    """
    изменение списка записей пользователя
    """
    template_name, form = None, None

    def get(self,request,*args,**kwargs):
        from common.template.user import get_detect_platform_template

        self.template_name = get_detect_platform_template("posts/post_user/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPostListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPostListEdit,self).get_context_data(**kwargs)
        context["list"] = PostList.objects.get(pk=self.kwargs["list_pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = PostList.objects.get(pk=self.kwargs["list_pk"])
        self.form = PostListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and self.list.creator.pk == request.user.pk:
            list = self.form.save(commit=False)
            new_list = list.edit_list(name=list.name, description=list.description, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPostListEdit,self).get(request,*args,**kwargs)


class UserPostListDelete(View):
    def get(self,request,*args,**kwargs):
        list = PostList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.type != PostList.MAIN and list.creator.pk == request.user.pk:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserPostListRecover(View):
    def get(self,request,*args,**kwargs):
        list = PostList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddPostInUserList(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        list = PostList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_item_in_list(post.pk):
            list.post_list.add(post)
            return HttpResponse()
        else:
            raise Http404

class RemovePostFromUserList(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        list = PostList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(post.pk):
            list.post_list.remove(post)
            return HttpResponse()
        else:
            raise Http404


class UserChangePosition(View):
    def post(self,request,*args,**kwargs):
        import json

        query = []

        for item in json.loads(request.body):
            post = Post.objects.get(pk=item['key'])
            post.order=item['value']
            post.save(update_fields=["order"])
            query += [post.pk, ]
        return HttpResponse(query)
