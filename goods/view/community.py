
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good, GoodAlbum
from communities.models import Community
from common.check.community import check_can_get_lists
from rest_framework.exceptions import PermissionDenied
from stst.models import GoodNumbers
from common.template.good import get_template_community_good, get_permission_community_good
from django.http import Http404


class CommunityGood(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.goods = self.album.get_goods()

        self.template_name = get_template_community_good(self.album.community, "goods/c_good/", "good.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityGood,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGood,self).get_context_data(**kwargs)
        context["object"] = self.good
        context["album"] = self.album
        context["community"] = self.album.community
        context["next"] = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
        context["prev"] = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
        return context


class GoodCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(pk=self.kwargs["good_pk"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() or not self.good.comments_enabled:
            raise Http404
        self.template_name = get_template_community_good(self.community, "goods/c_good_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.good
        context['community'] = self.community
        return context

    def get_queryset(self):
        check_can_get_lists(self.request.user, self.community)
        comments = self.good.get_comments()
        return comments
