
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from os.path import splitext
import uuid


def upload_to_post_image_directory(post_image, filename):
    post = post_image.post
    return _upload_to_post_directory_directory(post=post, filename=filename)

def upload_to_post_directory(post, filename):
    return _upload_to_post_directory_directory(post=post, filename=filename)

def _upload_to_post_directory_directory(post, filename):
    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()) + extension

    path = 'posts/%(post_uuid)s/' % {
        'post_uuid': str(post.uuid)}

    return '%(path)s%(new_filename)s' % {'path': path,
                                         'new_filename': new_filename, }


def paginate_data(qs, page_size, page, paginated_type, **kwargs):
    """Вспомогательная функция для превращения многих запросов в разбитые на страницы результаты по адресу
    избавьтесь от нашей конечной точки API GraphQL."""

    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)

    except PageNotAnInteger:
        page_obj = p.page(1)

    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )


class AuthorRequiredMixin(View):
    """Mixin для проверки, чем пользователь loggedin является создателем объекта
    для редактирования или обновления."""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.creator != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
