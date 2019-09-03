from rest_framework.exceptions import ValidationError
from common.utils.model_loaders import get_category_model


def category_name_exists(category_name):
    Category = get_category_model()
    if not Category.objects.filter(name=category_name).exists():
        raise ValidationError(
            'Категория с указанным именем не существует',
        )
