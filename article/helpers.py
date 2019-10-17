from users.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def upload_to_article_image_directory(article_profile, filename):
    article = article_profile.article
    return _upload_to_article_directory_directory(article=article, filename=filename)

def _upload_to_article_directory_directory(article, filename):
    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()) + extension

    path = 'article/%(article_uuid)s/' % {
        'article_uuid': str(article.uuid)}

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
