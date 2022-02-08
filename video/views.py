from video.models import VideoList, Video
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views import View
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
							)


class AllVideoView(ListView):
	template_name = "video.html"

	def get_queryset(self):
		return Video.objects.only("pk")


class LoadVideoList(ListView):
	template_name, c, paginate_by, is_user_can_see_video_section, is_user_can_see_video_list, is_user_can_create_videos = None, None, 10, None, None, None

	def get(self,request,*args,**kwargs):
		self.list = VideoList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.c = self.list.community
			if request.user.is_authenticated:
				if request.user.is_staff_of_community(self.c.pk):
					self.get_lists = VideoList.get_community_staff_lists(self.c.pk)
					self.is_user_can_see_video_section = True
					self.is_user_can_create_videos = True
					self.is_user_can_see_video_list = True
					self.template_name = get_template_community_list(self.list, "video/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
				else:
					self.get_lists = VideoList.get_community_lists(self.c.pk)
					self.is_user_can_see_video_section = self.c.is_user_can_see_video(request.user.pk)
					self.is_user_can_see_video_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_videos = self.list.is_user_can_create_el(request.user.pk)
			elif request.user.is_anonymous:
				self.template_name = get_template_anon_community_list(self.list, "video/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_video_section = self.c.is_anon_user_can_see_video()
				self.is_user_can_see_video_list = self.list.is_anon_user_can_see_el()
				self.get_lists = VideoList.get_community_lists(self.c.pk)
		else:
			if request.user.is_authenticated:
				if request.user.pk == self.list.creator.pk:
					creator = self.list.creator
					self.is_user_can_see_video_section = True
					self.is_user_can_see_video_list = True
					self.is_user_can_create_videos = True
				else:
					self.is_user_can_see_video_section = creator.is_user_can_see_video(request.user.pk)
					self.is_user_can_see_video_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_videos = self.list.is_user_can_create_el(request.user.pk)
				self.template_name = get_template_user_list(self.list, "video/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "video/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_video_section = creator.is_anon_user_can_see_good()
				self.is_user_can_see_video_list = self.list.is_anon_user_can_see_el()
		return super(LoadVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadVideoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.c
		context['is_user_can_see_video_section'] = self.is_user_can_see_video_section
		context['is_user_can_see_video_list'] = self.is_user_can_see_video_list
		context['is_user_can_create_videos'] = self.is_user_can_create_videos
		return context

	def get_queryset(self):
		return self.list.get_items()


class VideoCreate(TemplateView):
    template_name, form_post  = None, None
    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/create_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(VideoCreate,self).get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        from video.forms import VideoForm

        self.form_post = VideoForm(request.POST, request.FILES)
        self.list = VideoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form_post.is_valid() and list.is_user_can_create_el(request.user.pk):
            video = self.form_post.save(commit=False)
            new_video = video.create_video(creator=request.user,image=video.image, title=video.title,file=video.file,description=video.description,list=list,comments_enabled=video.comments_enabled,votes_on=video.votes_on,community=community)
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()
