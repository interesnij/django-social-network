from django.db import models
from users.models import User


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows',verbose_name="Подписчик")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=False,verbose_name="На кого подписывается")
