from django.views.generic.base import TemplateView
from communities.models import Community
from common.check.community import check_can_get_lists


class CommunityDetail(TemplateView):
    template_name,common_friends,common_friends_count, is_photo_open,is_post_open,is_members_open,is_doc_open,is_video_open,is_music_open,is_good_open = None,None,None,None,None,None,None,None,None,None

    def get(self,request,*args,**kwargs):
        from common.templates import update_activity, get_folder

        self.c, user_agent, r_user_pk = Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'], request.user.pk

        if request.user.is_authenticated:
            if request.user.type[0] == "_":
                if request.user.is_no_phone_verified():
                    template_name = "main/phone_verification.html"
                elif request.user.is_deleted():
                    template_name = "generic/u_template/you_deleted.html"
                elif request.user.is_closed():
                    template_name = "generic/u_template/you_closed.html"
                elif request.user.is_suspended():
                    template_name = "generic/u_template/you_suspended.html"
            elif self.c.type[0] == "_":
                if self.c.is_suspended():
                    if request_user.is_administrator_of_community(community.pk):
                        template_name = "generic/c_template/admin_community_suspended.html"
                    else:
                        template_name = "generic/c_template/community_suspended.html"
                elif self.c.is_deleted():
                    if request_user.is_administrator_of_community(community.pk):
                        template_name = "generic/c_template/admin_community_deleted.html"
                    else:
                        template_name = "generic/c_template/community_deleted.html"
                elif self.c.is_closed():
                    if request_user.is_administrator_of_community(community.pk):
                        template_name = "generic/c_template/admin_community_closed.html"
                    else:
                        template_name = "generic/c_template/community_closed.html"
            elif request.user.is_member_of_community(self.c.pk):
                if request.user.is_administrator_of_community(self.c.pk):
                    self.template_name = "communities/detail/admin_community.html"
                elif request.user.is_moderator_of_community(self.c.pk):
                    self.template_name = "communities/detail/moderator_community.html"
                elif request.user.is_editor_of_community(self.c.pk):
                    self.template_name = "communities/detail/editor_community.html"
                elif request.user.is_advertiser_of_community(self.c.pk):
                    self.template_name = "communities/detail/advertiser_community.html"
                elif request.user.is_community_manager():
                    self.template_name = "communities/detail/staff_member_community.html"
                else:
                    self.template_name = "communities/detail/member_community.html"
                request.user.create_or_plus_populate_community(self.c.pk)
            elif request.user.is_follow_from_community(self.c.pk):
                self.template_name = "communities/detail/follow_community.html"
            elif request.user.is_community_manager():
                self.template_name = "communities/detail/staff_community.html"
            elif request.user.is_banned_from_community(self.c.pk):
                self.template_name = "communities/detail/block_community.html"
            elif self.c.is_public():
                if request.user.is_child() and not self.c.is_verified():
                    self.template_name = "communities/detail/no_child_safety.html"
                else:
                    self.template_name = "communities/detail/public_community.html"
            elif self.c.is_close():
                self.template_name = "communities/detail/close_community.html"
            elif self.c.is_private():
                self.template_name = "generic/c_template/private_community.html"
            self.common_friends, self.common_friends_count = request.user.get_common_friends_of_community(self.c.pk)[0:6], request.user.get_common_friends_of_community_count_ru(self.c.pk)
            self.is_photo_open = self.c.is_user_can_see_photo(r_user_pk)
            self.is_post_open = self.c.is_user_can_see_post(r_user_pk)
            self.is_video_open = self.c.is_user_can_see_video(r_user_pk)
            self.is_music_open = self.c.is_user_can_see_music(r_user_pk)
            self.is_doc_open = self.c.is_user_can_see_doc(r_user_pk)
            self.is_member_open = self.c.is_user_can_see_member(r_user_pk)
            self.is_good_open = self.c.is_user_can_see_good(r_user_pk)

            update_activity(request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
        elif request.user.is_anonymous:
            if self.c.type[0] == "_":
                if self.c.is_suspended():
                    template_name = "generic/c_template/anon_community_suspended.html"
                elif self.c.is_deleted():
                    template_name = "generic/c_template/anon_community_deleted.html"
                elif self.c.is_closed():
                    template_name = "generic/c_template/anon_community_closed.html"
            elif self.c.is_public():
                if not self.c.is_verified():
                    self.template_name = "communities/detail/anon_no_child_safety.html"
                else:
                    self.template_name = "communities/detail/anon_community.html"
            elif self.c.is_closed():
                self.template_name = "communities/detail/anon_close_community.html"
            elif self.c.is_private():
                self.template_name = "communities/detail/anon_private_community.html"

            self.is_photo_open = self.c.is_anon_user_can_see_photo()
            self.is_video_open = self.c.is_anon_user_can_see_video()
            self.is_music_open = self.c.is_anon_user_can_see_music()
            self.is_doc_open = self.c.is_anon_user_can_see_doc()
            self.is_member_open = self.c.is_anon_user_can_see_member()
            self.is_good_open = self.c.is_anon_user_can_see_good()
            self.is_post_open = self.c.is_anon_user_can_see_post()

        self.template_name = get_folder(request.META['HTTP_USER_AGENT']) + self.template_name
        return super(CommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CommunityDetail,self).get_context_data(**kwargs)
        c["membersheeps"],c["community"],c["common_friends"],c["common_friends_count"],c['post_list_pk'],c['is_photo_open'],c['is_post_open'],c['is_member_open'],c['is_doc_open'],c['is_video_open'],c['is_music_open'],c['is_good_open'] = self.c.get_members(self.c.pk)[0:6],self.c,self.common_friends,self.common_friends_count,self.c.get_selected_post_list_pk(),self.is_photo_open,self.is_post_open,self.is_member_open,self.is_doc_open,self.is_video_open,self.is_music_open,self.is_good_open
        return c


class CommunityGallery(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_anon_community_list, get_template_community_list
        from gallery.models import PhotoList

        self.c = Community.objects.get(pk=self.kwargs["pk"])
        self.list = self.c.get_photo_list()
        if request.user.is_administrator_of_community(self.c.pk):
            self.get_lists = PhotoList.get_community_staff_lists(self.c.pk)
        else:
            self.get_lists = PhotoList.get_community_lists(self.c.pk)
        self.count_lists = PhotoList.get_community_lists_count(self.c.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_community_list(self.list, "communities/photos/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_community_list(self.list, "communities/photos/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityGallery,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CommunityGallery,self).get_context_data(**kwargs)
        c['community'], c['list'], c['get_lists'], c['count_lists'], c['is_admin'] = self.c, self.list, self.get_lists, self.count_lists, self.request.user.is_administrator_of_community(self.c.pk)
        return c

class CommunityPhotoList(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from gallery.models import PhotoList
        from common.templates import get_template_anon_community_list, get_template_community_list

        self.c, self.list = Community.objects.get(pk=self.kwargs["pk"]), PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_anonymous:
            self.template_name = get_template_anon_community_list(self.list, "communities/photos/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_community_list(self.list, "communities/photos/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])

        return super(CommunityPhotoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CommunityPhotoList,self).get_context_data(**kwargs)
        c['community'], c['list'] = self.c, self.list
        return c
