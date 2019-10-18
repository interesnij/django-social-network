from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo


class GalleryView(TemplateView):
	template_name="gallery.html"

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.albums=Album.objects.filter(creator=self.user)
		return super(GalleryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GalleryView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['albums'] = self.albums
		return context


class AlbomView(TemplateView):
	template_name="album.html"

	def get(self,request,*args,**kwargs):
		self.album=Album.objects.get(pk=self.kwargs["pk"])
		return super(AlbomView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(AlbomView,self).get_context_data(**kwargs)
		context['album'] = self.album
		return context

	def post_ajax(self, request, *args, **kwargs):
		try:
			album = Album.objects.get(pk=kwargs.get('pk'))
		except Album.DoesNotExist:
			error_dict = {'message': 'Album not found.'}
			return self.render_json_response(error_dict, status=404)

		uploaded_file = request.FILES['file']
		Photo.objects.create(album=album, file=uploaded_file)

		response_dict = {'message': 'File uploaded successfully!',}
		return self.render_json_response(response_dict, status=200)
