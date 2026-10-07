"""
SMTP email backend that reads its connection details from
Admin → Site Settings instead of settings.py / .env.
"""
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend


class SiteSettingsEmailBackend(SMTPEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        from core.models import SiteSettings

        site = SiteSettings.load()
        options = {
            'host': site.smtp_host,
            'port': site.smtp_port,
            'username': site.smtp_username,
            'password': site.smtp_password,
            'use_tls': site.smtp_use_tls,
            'use_ssl': site.smtp_use_ssl,
            'timeout': 20,
        }
        options.update({k: v for k, v in kwargs.items() if v is not None})
        super().__init__(fail_silently=fail_silently, **options)
