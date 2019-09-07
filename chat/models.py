from django.db import models


class ACategory(models.Model):
	name=models.CharField(max_length=100,db_index=True,unique=True,verbose_name="Название")
	order=models.PositiveSmallIntegerField(default=0,db_index=True,verbose_name="Порядковый номер")
	image=models.ImageField(blank=True, upload_to="a_category/list")
	def __str__(self):
		return self.name
	class Meta:
		ordering=["order","name"]
		verbose_name="категория статей"
		verbose_name_plural="категории статей"

	def __str__(self):
		return self.name
