from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from gallery.models import Photo, PhotoComment
from communities.models import Community
from common.model.votes import PhotoVotes, PhotoCommentVotes
from common.templates import get_template_user_item, get_template_anon_user_item, get_template_community_item, get_template_anon_community_item



class PhotoUserLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.photo, "gallery/photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.photo, "gallery/photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.photo.window_likes()
        context["text"] = "Фото одобрили:"
        context["class_name"] = "u_all_photo_likes"
        return context

class PhotoUserDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.photo, "gallery/photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.photo, "gallery/photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.photo.window_dislikes()
        context["text"] = "Фото не одобрили:"
        context["class_name"] = "u_all_photo_dislikes"
        return context


class PhotoUserCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.comment.get_item(), "gallery/photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.comment.get_item(), "gallery/photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Коммент одобрили:"
        context["class_name"] = "u_all_photo_comment_likes"
        return context


class PhotoUserCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.comment.get_item(), "gallery/photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.comment.get_item(), "gallery/photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Коммент не одобрили:"
        context["class_name"] = "u_all_photo_comment_dislikes"
        return context

class PhotoCommunityLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.photo.votes_on:
            if request.user.is_authenticated:
                self.template_name = get_template_community_item(self.photo, "gallery/photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_community_item(self.photo, "gallery/photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = "about.html"
        return super(PhotoCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.photo.window_likes()
        context["text"] = "Фото одобрили:"
        context["class_name"] = "c_all_photo_likes"
        return context

class PhotoCommunityDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.photo.votes_on:
            if request.user.is_authenticated:
                self.template_name = get_template_community_item(self.photo, "gallery/photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_community_item(self.photo, "gallery/photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = "about.html"
        return super(PhotoCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.photo.window_dislikes()
        context["text"] = "Фото не одобрили:"
        context["class_name"] = "u_all_photo_dislikes"
        return context

class PhotoCommunityCommentLikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.comment.get_item(), "gallery/photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.comment.get_item(), "gallery/photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"] = self.comment.window_likes()
        context["text"] = "Коммент одобрили:"
        context["class_name"] = "c_all_photo_comment_likes"
        return context

class PhotoCommunityCommentDislikeWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.comment.get_item(), "gallery/photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.comment.get_item(), "gallery/photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"] = self.comment.window_dislikes()
        context["text"] = "Коммент не одобрили:"
        context["class_name"] = "c_all_photo_comment_dislikes"
        return context


class AllPhotoUserLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.photo.votes_on:
            if request.user.is_authenticated:
                self.template_name = get_template_user_item(self.photo, "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_user_item(self.photo, "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = "about.html"
        return super(AllPhotoUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoUserLikeWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Фото одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.likes().values("user_id"))
        return users

class AllPhotoUserDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.photo.votes_on:
            if request.user.is_authenticated:
                self.template_name = get_template_user_item(self.photo, "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_user_item(self.photo, "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = "about.html"
        return super(AllPhotoUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoUserDislikeWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Фото не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.dislikes().values("user_id"))
        return users


class AllPhotoUserCommentLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.comment.get_item(), "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.comment.get_item(), "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.comment.get_item(), "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.comment.get_item(), "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.photo.votes_on:
            if request.user.is_authenticated:
                self.template_name = get_template_community_item(self.photo, "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_community_item(self.photo, "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = "about.html"
        return super(AllPhotoCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoCommunityLikeWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Фото одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.likes().values("user_id"))
        return users

class AllPhotoCommunityDislikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.photo.votes_on:
            if request.user.is_authenticated:
                self.template_name = get_template_community_item(self.photo, "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_community_item(self.photo, "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = "about.html"
        return super(AllPhotoCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoCommunityDislikeWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Фото не одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.dislikes().values("user_id"))
        return users


class AllPhotoCommunityCommentLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.comment.get_item(), "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.comment.get_item(), "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.comment.get_item(), "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.comment.get_item(), "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
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
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.photo, "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.photo, "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllPhotoCommunityRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoCommunityRepostWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Фото поделились:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.get_reposts().values("user_id"))
        return users

class AllPhotoUserRepostWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.photo, "gallery/all_photo_votes/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.photo, "gallery/all_photo_votes/anon_page.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllPhotoUserRepostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPhotoUserRepostWindow,self).get_context_data(**kwargs)
        context['photo'] = self.photo
        context['text'] = "Фото одобрили:"
        return context

    def get_queryset(self):
        users = User.objects.filter(id__in=self.photo.get_reposts().values("user_id"))
        return users
