import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good
from communities.models import Community
from common.checkers import check_can_get_posts_for_community_with_name
from rest_framework.exceptions import PermissionDenied
from stst.models import GoodNumbers


class CommunityGoods(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_template(folder="c_good/", template="goods.html", request=request)
        return super(CommunityGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGoods,self).get_context_data(**kwargs)
        context["community"] = self.community
        return context

    def get_queryset(self):
        if self.request.user.is_staff_of_community_with_name(self.community.name):
            goods_list = self.community.get_admin_goods().order_by('-created')
        else:
            goods_list = self.community.get_goods().order_by('-created')
        return goods_list


class CommunityGood(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(uuid=self.kwargs["uuid"])
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.goods = self.user.get_goods()

        if request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_good/admin_good.html"
                self.goods = self.user.get_admin_goods()
            elif request.user.is_post_manager():
                self.template_name = "c_lenta/staff_good.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_lenta/good.html"
            else:
                self.template_name = "c_lenta/good.html"
            try:
                GoodNumbers.objects.filter(user=request.user.pk, good=self.good.pk).exists()
            except:
                if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                    GoodNumbers.objects.create(user=request.user.pk, good=self.good.pk, platform=0)
                else:
                    GoodNumbers.objects.create(user=request.user.pk, good=self.good.pk, platform=1)
        elif request.user.is_anonymous:
            if self.community.is_public():
                self.template_name = "c_lenta/anon_good.html"
            else:
                self.template_name = "c_good/anon_close_good.html"

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        self.next = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
        self.prev = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
        return super(CommunityGood,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGood,self).get_context_data(**kwargs)
        context["object"] = self.good
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context


class GoodCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if not self.good.comments_enabled:
            raise PermissionDenied('Комментарии для фотографии отключены')
        elif request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_good_comment/admin_comments.html"
            elif request.user.is_good_manager():
                self.template_name = "c_good_comment/staff_comments.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_good_comment/comments.html"
            else:
                self.template_name = "c_good_comment/comments.html"
        elif request.user.is_anonymous:
            if self.is_public():
                self.template_name = "c_good_comment/anon_comments.html"
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(GoodCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.good
        context['community'] = self.community
        return context

    def get_queryset(self):
        check_can_get_posts_for_community_with_name(self.request.user, self.community.name)
        comments = self.good.get_comments()
        return comments
