from django.views.generic.base import TemplateView
from communities.models import Community
from common.check.community import check_can_get_lists
from common.templates import get_template_anon_community_list, get_template_community_list


class CommunityDetail(TemplateView):
    template_name,common_friends,common_friends_count,is_photo_open,is_post_open,\
    is_member_open,is_doc_open,is_video_open,is_music_open,is_good_open,is_message_open,\
    is_settings_open,is_stat_open,is_staff,is_manager = None,\
    None,None,None,None,None,None,None,None,None,None,None,None,None,None

    def get(self,request,*args,**kwargs):
        from common.templates import update_activity, get_folder

        self.c, user_agent, r_user_pk = Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'], request.user.pk

        if request.user.is_authenticated:
            if request.user.type[0] == "_":
                if request.user.is_deleted():
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
                self.template_name = "communities/detail/public_community.html"
                request.user.plus_community_visited(self.c.pk)
            elif request.user.is_follow_from_community(self.c.pk):
                self.template_name = "communities/detail/follow_community.html"
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

            if request.user.pk == self.c.creator.pk:
                self.is_stat_open,self.is_settings_open,self.is_message_open,self.is_photo_open,self.is_post_open,self.is_member_open,self.is_doc_open,self.is_video_open,self.is_music_open,self.is_good_open = True,True,True,True,True,True,True,True,True,True
            else:
                self.is_photo_open = self.c.is_user_can_see_photo(r_user_pk)
                self.is_post_open = self.c.is_user_can_see_post(r_user_pk)
                self.is_video_open = self.c.is_user_can_see_video(r_user_pk)
                self.is_music_open = self.c.is_user_can_see_music(r_user_pk)
                self.is_doc_open = self.c.is_user_can_see_doc(r_user_pk)
                self.is_member_open = self.c.is_user_can_see_member(r_user_pk)
                self.is_good_open = self.c.is_user_can_see_good(r_user_pk)
                self.is_message_open = self.c.is_user_can_send_message(r_user_pk)
                self.is_settings_open = self.c.is_user_can_see_settings(r_user_pk)
                self.is_stat_open = self.c.is_user_can_see_stat(r_user_pk)
            self.is_staff =  request.user.is_staff_of_community(self.c.pk)
            self.is_manager =  request.user.is_manager()

            update_activity(request.user, request.META['HTTP_USER_AGENT'])
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
            self.is_stat_open = self.c.is_anon_user_can_see_stat()

        self.template_name = get_folder(request.META['HTTP_USER_AGENT']) + self.template_name
        return super(CommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CommunityDetail,self).get_context_data(**kwargs)
        c["membersheeps"],c["community"],c["common_friends"],c["common_friends_count"],\
        c['post_list_pk'],c['is_photo_open'],c['is_post_open'],c['is_member_open'],\
        c['is_doc_open'],c['is_video_open'],c['is_music_open'],\
        c['is_good_open'], c['is_message_open'], c['is_manager'], \
        c['is_settings_open'], c['is_stat_open'], c['is_staff'] = self.c.get_members(self.c.pk)[0:6],self.c,self.common_friends,\
        self.common_friends_count,self.c.get_selected_post_list_pk(),self.is_photo_open,\
        self.is_post_open,self.is_member_open,self.is_doc_open,self.is_video_open,\
        self.is_music_open,self.is_good_open,self.is_message_open,\
        self.is_manager, self.is_settings_open, self.is_stat_open, \
        self.is_staff
        return c


class CommunityGallery(TemplateView):
    template_name, is_user_can_see_photo_section = None, None

    def get(self,request,*args,**kwargs):
        from gallery.models import PhotoList

        self.c = Community.objects.get(pk=self.kwargs["pk"])
        self.list = self.c.get_photo_list()
        if request.user.is_administrator_of_community(self.c.pk):
            self.get_lists = PhotoList.get_community_staff_lists(self.c.pk)
            self.is_user_can_see_photo_section = True
        else:
            self.get_lists = PhotoList.get_community_lists(self.c.pk)
            self.is_user_can_see_photo_section = self.c.is_user_can_see_photo()
        self.count_lists = PhotoList.get_community_lists_count(self.c.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_community_list(self.list, "communities/photos/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_photo_section = self.user.is_anon_user_can_see_photo()
        else:
            self.template_name = get_template_community_list(self.list, "communities/photos/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityGallery,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CommunityGallery,self).get_context_data(**kwargs)
        c['community'], c['list'], c['get_lists'], c['count_lists'], \
        c['is_user_can_see_photo_section'], c['photo_list_pk'] = self.c, self.list, self.get_lists, \
        self.count_lists, self.is_user_can_see_photo_section, self.c.get_selected_photo_list_pk()
        return c

class CommunityPhotoList(TemplateView):
    template_name, is_user_can_see_photo_section = None, None

    def get(self,request,*args,**kwargs):
        from gallery.models import PhotoList

        self.c, self.list = Community.objects.get(pk=self.kwargs["pk"]), PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_administrator_of_community(self.c.pk):
            self.is_user_can_see_photo_section = True
        else:
            self.is_user_can_see_photo_section = self.c.is_user_can_see_photo()
        if request.user.is_anonymous:
            self.template_name = get_template_anon_community_list(self.list, "communities/photos/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_photo_section = self.user.is_anon_user_can_see_photo()
        else:
            self.template_name = get_template_community_list(self.list, "communities/photos/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])

        return super(CommunityPhotoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CommunityPhotoList,self).get_context_data(**kwargs)
        c['community'], c['list'], c['is_user_can_see_photo_section'] = self.c, self.list, self.is_user_can_see_photo_section
        return c
