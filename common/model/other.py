from django.db import models
from django.conf import settings


class PhoneCodes(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    code = models.PositiveSmallIntegerField(default=0, verbose_name="Код")

class CustomLink(models.Model):
    link = models.CharField(max_length=32, unique=True, verbose_name="Название ссылки, уникально для П. и С.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='user_link', verbose_name="Пользователь")
    #community = models.ForeignKey('communities.Community', blank=True, null=True, on_delete=models.CASCADE, related_name='community_link', verbose_name="Сообщество")

    class Meta:
        verbose_name = 'Пользовательская ссылка'
        verbose_name_plural = 'Пользовательские ссылки'

    def __str__(self):
        if self.user:
            return '{} - {}'.format(self.user, self.link)
        elif self.community:
            return '{} - {}'.format(self.community, self.link)
        else:
            return self.link

    def get_user_pk(self):
        return self.user.pk

class StickerCategory(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="Название")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='+', verbose_name="Пользователь")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = 'Категория стикеров'
        verbose_name_plural = 'Категории стикеров'

    def __str__(self):
        return self.name

    def get_stickers(self):
        from common.model.other import Stickers
        return Stickers.objects.filter(category_id=self.pk)

class Stickers(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="Название")
    category = models.ForeignKey(StickerCategory, on_delete=models.CASCADE, related_name='+', verbose_name="Категория")
    image = models.ImageField(upload_to="stickers/")

    class Meta:
        verbose_name = 'Стикер'
        verbose_name_plural = 'Стикеры'

    def __str__(self):
        return self.name


class SmileCategory(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="Название")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

    class Meta:
        verbose_name = 'Категория смайликов'
        verbose_name_plural = 'Категории смайликов'

    def __str__(self):
        return self.name

    def get_smiles(self):
        from common.model.other import Smiles
        return Smiles.objects.filter(category_id=self.pk)


class Smiles(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="Название")
    category = models.ForeignKey(SmileCategory, on_delete=models.CASCADE, related_name='+', verbose_name="Категория")
    image = models.ImageField(upload_to="smiles/")

    class Meta:
        verbose_name = 'Смайл'
        verbose_name_plural = 'Смайлы'

    def __str__(self):
        return self.name

class UserPopulateSmiles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', verbose_name="Пользователь")
    smile = models.ForeignKey(Smiles, on_delete=models.CASCADE, related_name='smile', verbose_name="Смайл")
    count = models.PositiveIntegerField(default=1, verbose_name="Количество использований пользователем")

    class Meta:
        verbose_name = 'Популярность смайликов'
        verbose_name_plural = 'Популярность смайликов'
        ordering = ['-count']

    def __str__(self):
        return self.user.get_full_name()

    def get_plus_or_create(user_pk, smile_pk):
        if UserPopulateSmiles.objects.filter(user_id=user_pk, smile_id=smile_pk).exists():
            md = UserPopulateSmiles.objects.get(user_id=user_pk, smile_id=smile_pk)
            md.count += 1
            md.save(update_fields=["count"])
        else:
            UserPopulateSmiles.objects.create(user_id=user_pk, smile_id=smile_pk)


class UserPopulateStickers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', verbose_name="Пользователь")
    sticker = models.ForeignKey(Stickers, on_delete=models.CASCADE, related_name='sticker', verbose_name="Стикер")
    count = models.PositiveIntegerField(default=1, verbose_name="Количество использований пользователем")

    class Meta:
        verbose_name = 'Популярность стикеров'
        verbose_name_plural = 'Популярность стикеров'
        ordering = ['-count']

    def __str__(self):
        return self.user.get_full_name()

    def get_plus_or_create(user_pk, sticker_pk):
        if UserPopulateStickers.objects.filter(user_id=user_pk, sticker_id=sticker_pk).exists():
            md = UserPopulateStickers.objects.get(user_id=user_pk, sticker_id=sticker_pk)
            md.count += 1
            md.save(update_fields=["count"])
        else:
            UserPopulateStickers.objects.create(user_id=user_pk, sticker_id=sticker_pk)
