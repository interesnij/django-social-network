import uuid
from django.db import models
from users.models import User
from django.contrib.contenttypes.fields import GenericRelation
from goods.helpers import upload_to_good_image_directory
from main.models import LikeDislike
from pilkit.processors import ResizeToFill, ResizeToFit
from moderation.models import ModeratedObject
from imagekit.models import ProcessedImageField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notifications.models.notification import Notification, notification_handler
from django.utils import timezone



class GoodCategory(models.Model):
	name=models.CharField(max_length=100,db_index=True,verbose_name="Название категории")
	order=models.PositiveSmallIntegerField(default=0,db_index=True,verbose_name="Порядковый номер")
	image=models.ImageField(blank=True, verbose_name="Изображение", upload_to="goods/list")

	def __str__(self):
		return self.name

	class Meta:
		ordering=["order","name"]
		verbose_name="категория товаров"
		verbose_name_plural="категории товаров"


class GoodSubCategory(models.Model):
	name=models.CharField(max_length=100,db_index=True,verbose_name="Название подкатегории")
	order=models.PositiveSmallIntegerField(default=0,db_index=True,verbose_name="Порядковый номер подкатегории")
	category=models.ForeignKey(GoodCategory,on_delete=models.CASCADE, verbose_name="Категория-родитель")
	image=models.ImageField(blank=True, verbose_name="Изображение",upload_to="sub_category/list")

	def __str__(self):
		return self.name

class Good(models.Model):

    class Meta:
        verbose_name="Товар"
        verbose_name_plural="Товары"

    moderated_object = GenericRelation(ModeratedObject, related_query_name='goods')
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(max_length=1000, verbose_name="Описание товара")
	community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='good',null=True,blank=True,verbose_name="Сообщество")
    price = models.PositiveIntegerField(default=0, verbose_name="Цена товара")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    sub_category = models.ForeignKey(GoodSubCategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
    img0 = models.ImageField(upload_to="goods/%Y/%m/%d", blank=True)
    img1 = models.ImageField(upload_to="goods/%Y/%m/%d", blank=True)
    img2 = models.ImageField(upload_to="goods/%Y/%m/%d", blank=True)
    img3 = models.ImageField(upload_to="goods/%Y/%m/%d", blank=True)
    img4 = models.ImageField(upload_to="goods/%Y/%m/%d", blank=True)
    img5 = models.ImageField(upload_to="goods/%Y/%m/%d", blank=True)
    img6 = models.ImageField(upload_to="goods/%Y/%m/%d", blank=True)
    img7 = models.ImageField(upload_to="goods/%Y/%m/%d", blank=True)
    views=models.IntegerField(default=0,verbose_name="Просмотры")
    votes = GenericRelation(LikeDislike, related_query_name='good')
    is_active=models.BooleanField(default=False, verbose_name='Товар активен')
    is_sold=models.BooleanField(default=False, verbose_name='Товар не актуален')
    created=models.DateTimeField(default=timezone.now,db_index=True,verbose_name="Опубликованo")
    is_reklama=models.BooleanField(default=False, verbose_name='Это реклама')

    def __str__(self):
        return self.title

    def notification_like(self, user):
        notification_handler(user, self.creator,Notification.LIKED, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_dislike(self, user):
        notification_handler(user, self.creator,Notification.DISLIKED, action_object=self,id_value=str(self.uuid),key='social_update')

    def notification_comment(self, user):
        notification_handler(user, self.creator,Notification.POST_COMMENT, action_object=self,id_value=str(self.uuid),key='notification')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        channel_layer = get_channel_layer()
        payload = {
                "type": "receive",
                "key": "additional_good",
                "actor_name": self.creator.get_full_name()

            }
        async_to_sync(channel_layer.group_send)('notifications', payload)
