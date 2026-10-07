from django.db import models

from core.icons import ICON_CHOICES

from .base import OrderedItem, SingletonModel, image_field


class AboutSection(SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    section_label = models.CharField('Small label above heading', max_length=50, blank=True, default='ABOUT LIT')
    heading = models.CharField('Heading', max_length=200, default='More Than a WhatsApp Group.')
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=200, blank=True, default='A Community.',
        help_text='Shown in the accent colour (italic) after the heading.',
    )
    paragraph_1 = models.TextField('First paragraph', blank=True)
    paragraph_2 = models.TextField('Second paragraph', blank=True)

    background_image = image_field(
        'about', 'Section background image', 'The patterned background behind the whole section.',
    )

    image = image_field('about', 'Photo', 'Portrait photo shown on the left, about 800x1000 px.')
    image_alt_text = models.CharField('Photo description', max_length=200, blank=True)
    badge_title = models.CharField(
        'Photo badge - big text', max_length=50, blank=True, default='தமிழ்',
        help_text='The small card on the corner of the photo. Leave empty to hide it.',
    )
    badge_subtitle = models.CharField('Photo badge - small text', max_length=50, blank=True, default='ONE COMMUNITY')

    class Meta:
        verbose_name = 'About Section'
        verbose_name_plural = 'About Section'

    def __str__(self):
        return 'About Section'

    @property
    def active_pillars(self):
        return self.pillars.filter(is_active=True)


class AboutPillar(OrderedItem):
    about = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='pillars')
    icon = models.CharField('Icon', max_length=50, choices=ICON_CHOICES, default='users')
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description', blank=True)
    is_highlighted = models.BooleanField(
        'Highlight', default=False,
        help_text='Keeps the gold border and gold title on all the time (normally they only show on hover).',
    )

    class Meta(OrderedItem.Meta):
        verbose_name = 'Card'
        verbose_name_plural = 'Cards (Connect / Support / Celebrate) - numbers 01, 02, 03 are added automatically'

    def __str__(self):
        return self.title
