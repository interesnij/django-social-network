from django.db import models
from django.conf import settings


class Connection(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='connections',verbose_name="Кто связывается")
    target_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='targeted_connections', null=False,verbose_name="С кем связывается")
    target_connection = models.OneToOneField('self', on_delete=models.CASCADE, null=True,verbose_name="Связь")
