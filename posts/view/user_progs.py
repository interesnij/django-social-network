from users.models import User
from posts.models import *
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View
from posts.forms import *
from django.http import Http404
from django.views.generic.base import TemplateView


class PostUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post, user, lists, attach = PostForm(request.POST), User.objects.get(pk=self.kwargs["pk"]), request.POST.getlist("lists"), request.POST.getlist('attach_items')

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)

            if request.POST.get('text') or attach:
                from common.template.user import render_for_platform

                new_post = post.create_post(creator=request.user, text=post.text, community=None, category=post.category, lists=lists, attach=attach, parent=None, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
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
                return HttpResponse()
            if PostNumbers.objects.filter(user=request.user.pk, post=post.pk).exists():
                return HttpResponse()
            else:
                PostNumbers.objects.create(user=request.user.pk, post=post.pk, device=request.user.get_device())
                return HttpResponse()
        else:
            return HttpResponse()

class UserAdPostView(View):
    def get(self,request,*args,**kwargs):
        from stst.models import PostAdNumbers

        if request.is_ajax() and request.user.is_authenticated:
            post = Post.objects.get(uuid=self.kwargs["uuid"])
            if PostNumbers.objects.filter(user=request.user.pk, post=post.pk).exists():
                return HttpResponse()
            else:
                PostAdNumbers.objects.get(user=request.user.pk, post=post.pk, device=request.user.get_device())
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
                from common.notify.notify import user_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, post=post, text=comment.text)
                user_notify(request.user, post.creator.pk, None, "com"+str(new_comment.pk)+", pos"+str(post.pk), "u_post_comment_notify", "COM")
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
                from common.notify.notify import user_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, post=None, text=comment.text)
                user_notify(request.user, parent.post.creator.pk, None, "rep"+str(new_comment.pk)+",com"+str(parent.pk)+",pos"+str(parent.post.pk), "u_post_comment_notify", "REP")
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'posts/u_post_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class PostCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.is_ajax() and request.user.pk == int(self.kwargs["pk"]):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostWallCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.is_ajax() and request.user.pk == int(self.kwargs["pk"]):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
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
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user == item.creator and request.is_ajax():
            item.comments_enabled = False
            item.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostUserOnComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user == item.creator and request.is_ajax():
            item.comments_enabled = True
            item.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostUserDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == item.creator.pk:
            item.is_deleted = True
            item.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostWallUserDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == int(self.kwargs["pk"]):
            item.is_deleted = True
            item.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == item.creator.pk:
            item.is_deleted = False
            item.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class PostWallUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == int(self.kwargs["pk"]):
            item.is_deleted = False
            item.save(update_fields=['is_deleted'])
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
    """
    создание списка записей пользователя
    """
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
            list.creator = request.user
            list.type = PostList.LIST
            if list.order < 1:
                list.order = 1
            list.save()
            return render_for_platform(request, 'users/lenta/my_list.html',{'list': list})
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
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            if list.order < 1:
                list.order = 1
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPostListEdit,self).get(request,*args,**kwargs)


class UserPostListDelete(View):
    def get(self,request,*args,**kwargs):
        list = PostList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.type == PostList.LIST and list.creator.pk == request.user.pk:
            list.is_deleted = True
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserPostListAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = PostList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.is_deleted = False
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404
