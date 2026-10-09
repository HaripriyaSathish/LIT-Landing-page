from django.db import models
from django.utils import timezone

from .base import SingletonModel


class Footer(SingletonModel):
    brand_name = models.CharField('Organisation name', max_length=100, default='LONDON INDIAN TAMILS')
    tagline = models.CharField('Tagline', max_length=150, blank=True, default='CONNECT • SUPPORT • CELEBRATE')
    quote = models.CharField(
        'Quote', max_length=200, blank=True,
        default='India in our heart. London in our home. Tamil in our identity.',
    )
    show_social_icons = models.BooleanField(
        'Show social media icons', default=True,
        help_text='Icons come from Social Media Section → accounts ticked "Show in footer".',
    )
    copyright_text = models.CharField(
        'Copyright text', max_length=200, default='London Indian Tamils. All Rights Reserved.',
        help_text='"© <current year>" is added in front automatically.',
    )
    show_credit = models.BooleanField('Show designer credit', default=True)
    credit_text = models.CharField(
        'Credit text', max_length=150, blank=True, default='Designed & Developed by Vetri IT Systems',
        help_text='Small line under the copyright. The whole line is a link.',
    )
    credit_link = models.URLField(
        'Credit link', max_length=500, blank=True, default='https://vetriitsystems.com/',
        help_text='Opens in a new tab.',
    )

    class Meta:
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer'

    def __str__(self):
        return 'Footer'

    @property
    def copyright(self):
        return f'© {timezone.now().year} {self.copyright_text}'

    @property
    def page_links(self):
        from .pages import InfoPage

        return InfoPage.objects.filter(is_active=True, show_in_footer=True)

    @property
    def social_links(self):
        from .social import SocialLink

        if not self.show_social_icons:
            return SocialLink.objects.none()
        return SocialLink.objects.filter(is_active=True, show_in_footer=True).order_by('footer_order', 'id')
