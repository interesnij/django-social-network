from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from gallery.models import Photo, PhotoComment
from communities.models import Community
from common.model.votes import PhotoVotes, PhotoCommentVotes


class PhotoUserLikeWindow(TemplateView):
    template_name="photo_votes/u_like.html"

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.creator.get_permission_list_user(folder="photo_votes/", template="page.html", request=request)
        return super(PhotoUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.photo.window_likes()
        context["text"] = "Оценили:"
        context["class_name"] = "u_all_photo_likes"
        return context

class PhotoUserDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.creator.get_permission_list_user(folder="photo_votes/", template="page.html", request=request)
        return super(PhotoUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.photo.window_dislikes()
        context["text"] = "Не оценили:"
        context["class_name"] = "u_all_photo_dislikes"
        return context


class PhotoUserCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="photo_votes/", template="page.html", request=request)
        return super(PhotoUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Оценили:"
        context["class_name"] = "u_all_photo_comment_likes"
        return context


class PhotoUserCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="photo_votes/", template="page.html", request=request)
        return super(PhotoUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Не оценили:"
        context["class_name"] = "u_all_photo_comment_dislikes"
        return context

class PhotoCommunityLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.community.get_template_list(folder="photo_votes/", template="page.html", request=request)
        return super(PhotoCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.photo.window_likes()
        context["text"] = "Оценили:"
        context["class_name"] = "c_all_photo_likes"
        return context

class PhotoCommunityDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.community.get_template_list(folder="photo_votes/", template="page.html", request=request)
        return super(PhotoCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.photo.window_dislikes()
        context["text"] = "Не оценили:"
        context["class_name"] = "u_all_photo_dislikes"
        return context

class PhotoCommunityCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.community.get_template_list(folder="photo_votes/", template="page.html", request=request)
        return super(PhotoCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Оценили:"
        context["class_name"] = "c_all_photo_comment_likes"
        return context

class PhotoCommunityCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.community.get_template_list(folder="photo_votes/", template="page.html", request=request)
        return super(PhotoCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Не оценили:"
        context["class_name"] = "c_all_photo_comment_dislikes"
        return context


class AllPhotoUserLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.creator.get_permission_list_user(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoUserLikeWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Запись одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.likes().values("user_id"))
        return users

class AllPhotoUserDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.creator.get_permission_list_user(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoUserDislikeWindow,self).get_context_data(**kwargs)
        context['item'] = self.photo
        context['text'] = "Запись не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.dislikes().values("user_id"))
        return users


class AllPhotoUserCommentLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoUserCommentLikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.likes().values("user_id"))
        return users


class AllPhotoUserCommentDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.commenter.get_permission_list_user(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.dislikes().values("user_id"))
        return users


class AllPhotoCommunityLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.community.get_template_list(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoCommunityLikeWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Запись одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.likes().values("user_id"))
        return users

class AllPhotoCommunityDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.community.get_template_list(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoCommunityDislikeWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Запись не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.dislikes().values("user_id"))
        return users


class AllPhotoCommunityCommentLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.photo.community.get_template_list(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.likes().values("user_id"))
        return users


class AllPhotoCommunityCommentDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        self.template_name = self.comment.photo.community.get_template_list(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context['comment'] = self.comment
        context['text'] = "Комментарий не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.comment.dislikes().values("user_id"))
        return users


class AllPhotoCommunityRepostWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.community.get_template_list(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoCommunityRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoCommunityRepostWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Записью поделились:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.get_reposts().values("user_id"))
        return users

class AllPhotoUserRepostWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.photo.creator.get_permission_list_user(folder="all_photo_votes/", template="page.html", request=request)
        return super(AllPhotoUserRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoUserRepostWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Запись одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.get_reposts().values("user_id"))
        return users
