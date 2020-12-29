from django.db import models
from django.conf import settings


class PhoneCodes(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    code = models.PositiveSmallIntegerField(default=0, verbose_name="Код")
    id = models.BigAutoField(primary_key=True)


class CustomLink(models.Model):
    link = models.CharField(max_length=32, unique=True, verbose_name="Название сслыки, уникально для П. и С.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE, related_name='user_link', verbose_name="Пользователь")
    community = models.ForeignKey('communities.Community', blank=True, on_delete=models.CASCADE, related_name='community_link', verbose_name="Сообщество")

    class Meta:
        verbose_name = 'Пользовательская ссылка'
        verbose_name_plural = 'Пользовательские ссылки'

    def __str__(self):
        if self.user:
            return ''.join([self.user.get_full_name, ' - ', self.link])
        elif self.community:
            return ''.join([self.community.name, ' - ', self.link])
        else:
            return self.link
