from common.models import ProxyBlacklistDomain
from rest_framework.exceptions import PermissionDenied


def check_url_can_be_proxied(url):
    urls = extract_urls_from_string(url)

    if not urls:
        raise PermissionDenied(
            'Не указан действительный URL-адрес',
        )
    if ProxyBlacklistDomain.is_url_domain_blacklisted(url):
        raise PermissionDenied(
            'Url-адрес занесен в черный список',
        )
