from django.db import models

from .base import OrderedItem, SharedBackgroundMixin, SingletonModel, image_field


class SocialSection(SharedBackgroundMixin, SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    background_image = image_field(
        'social', 'Section background image', SharedBackgroundMixin.SHARED_BACKGROUND_HELP,
    )
    section_label = models.CharField('Small label above heading', max_length=50, blank=True, default='SOCIAL MEDIA')
    heading = models.CharField('Heading', max_length=200, default='Stay Connected')
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=200, blank=True, default='With LIT',
        help_text='Shown in the accent colour (italic) on the line below the heading.',
    )
    description = models.TextField(
        'Description', blank=True,
        default='Follow us for community news, event announcements, photos, videos and activities.',
    )

    class Meta:
        verbose_name = 'Social Media Section'
        verbose_name_plural = 'Social Media Section'

    def __str__(self):
        return 'Social Media Section'

    @property
    def active_links(self):
        return self.links.filter(is_active=True)


class SocialLink(OrderedItem):
    """A social media account. Also used for the icons in the footer."""

    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
        ('x', 'X (Twitter)'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
    ]

    section = models.ForeignKey(SocialSection, on_delete=models.CASCADE, related_name='links')
    platform = models.CharField('Platform', max_length=20, choices=PLATFORM_CHOICES, help_text='Sets the icon.')
    label = models.CharField('Small label', max_length=50, blank=True, help_text='e.g. INSTAGRAM')
    account_name = models.CharField('Account name', max_length=100, help_text='e.g. @londonindiantamils')
    url = models.URLField(
        'Link', max_length=500, blank=True,
        help_text='Full address of the page, e.g. https://www.facebook.com/...',
    )
    show_in_footer = models.BooleanField('Show in footer', default=True)
    footer_order = models.PositiveIntegerField('Footer order', default=0, help_text='Order of the icons in the footer.')

    class Meta(OrderedItem.Meta):
        verbose_name = 'Social account'
        verbose_name_plural = 'Social accounts'

    ICONS = {
        'instagram': 'instagram', 'facebook': 'facebook', 'youtube': 'youtube',
        'whatsapp': 'message-circle', 'x': 'twitter', 'linkedin': 'linkedin', 'tiktok': 'music-2',
    }

    def __str__(self):
        return f'{self.get_platform_display()} - {self.account_name}'

    @property
    def icon(self):
        return self.ICONS.get(self.platform, 'link')
