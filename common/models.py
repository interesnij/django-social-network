from django.db import models
import tldextract
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum
from django.conf import settings
from main.models import Item


class ProxyBlacklistedDomain(models.Model):
    domain = models.CharField(max_length=100, unique=True)

    @classmethod
    def is_url_domain_blacklisted(cls, url):
        url = url.lower()
        if not urlparse(url).scheme:
            url = 'http://' + url
        tld_extract_result = tldextract.extract(url)
        url_root_domain = '.'.join([tld_extract_result.domain, tld_extract_result.suffix])
        url_full_domain = '.'.join([tld_extract_result.subdomain, tld_extract_result.domain, tld_extract_result.suffix])
        return cls.objects.filter(Q(domain=url_root_domain) | Q(domain=url_full_domain)).exists()


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def posts(self):
        return self.get_queryset().filter(content_type__model='items').order_by('-item__created')
    def comments(self):
        return self.get_queryset().filter(content_type__model='comments').order_by('-comment__created')

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.PositiveIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    objects = LikeDislikeManager()
