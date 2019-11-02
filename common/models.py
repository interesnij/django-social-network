from django.db import models
import tldextract
from django.db.models import Q


class EmojiGroup(models.Model):
    keyword = models.CharField(max_length=32, blank=False, null=False)
    order = models.IntegerField(unique=False, default=100)
    created = models.DateTimeField(editable=False)
    is_reaction_group = models.BooleanField(default=False)

    def __str__(self):
        return 'EmojiGroup: ' + self.keyword

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(EmojiGroup, self).save(*args, **kwargs)

    class Meta:
        verbose_name="группа смайликоа"
        verbose_name_plural="группы смайликов"


class Emoji(models.Model):
    group = models.ForeignKey(EmojiGroup, on_delete=models.CASCADE, related_name='emojis', null=True)
    keyword = models.CharField(max_length=16, blank=False, null=False)
    image = models.ImageField(blank=False, null=False, upload_to="emoji/")
    created = models.DateTimeField(editable=False)
    order = models.IntegerField(unique=False, default=100)

    def __str__(self):
        return 'Emoji: ' + self.keyword

    class Meta:
        verbose_name="смайлик"
        verbose_name_plural="смайлики"

    @classmethod
    def get_emoji_comment(cls, post_comment_id, emoji_id=None, reactor_id=None):
        emoji_query = Q(post_comment_reactions__post_comment_id=post_comment_id, )

        if emoji_id:
            emoji_query.add(Q(post_comment_reactions__emoji_id=emoji_id), Q.AND)

        if reactor_id:
            emoji_query.add(Q(post_comment_reactions__reactor_id=reactor_id), Q.AND)

        emojis = Emoji.objects.filter(emoji_query).annotate(Count('post_comment_reactions')).distinct().order_by(
            '-post_comment_reactions__count').all()

        return [{'emoji': emoji, 'count': emoji.post_comment_reactions__count} for emoji in emojis]

    @classmethod
    def get_emoji(cls, item_id, emoji_id=None, reactor_id=None):
        emoji_query = Q(post_reactions__item_id=item_id, )

        if emoji_id:
            emoji_query.add(Q(post_reactions__emoji_id=emoji_id), Q.AND)

        if reactor_id:
            emoji_query.add(Q(post_reactions__reactor_id=reactor_id), Q.AND)

        emojis = Emoji.objects.filter(emoji_query).annotate(Count('post_reactions')).distinct().order_by(
            '-post_reactions__count').all()

        return [{'emoji': emoji, 'count': emoji.post_reactions__count} for emoji in emojis]


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
