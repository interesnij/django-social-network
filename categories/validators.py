from rest_framework.exceptions import ValidationError


def category_name_exists(category_name):
    Category = get_category_model()
    if not Category.objects.filter(name=category_name).exists():
        raise ValidationError(
            'Категория с указанным именем не существует',
        )
