from django.db import models

from core.icons import ICON_CHOICES

from .base import OrderedItem, SharedBackgroundMixin, SingletonModel, image_field


class CommunitySection(SharedBackgroundMixin, SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    background_image = image_field(
        'community', 'Section background image',
        SharedBackgroundMixin.SHARED_BACKGROUND_HELP,
    )
    section_label = models.CharField('Small label above heading', max_length=50, blank=True, default='OUR COMMUNITY')
    heading = models.CharField('Heading', max_length=200, default="There's Something")
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=200, blank=True, default='for Everyone',
        help_text='Shown in the accent colour (italic) after the heading.',
    )

    class Meta:
        verbose_name = 'Community Section'
        verbose_name_plural = 'Community Section'

    def __str__(self):
        return 'Community Section'

    @property
    def active_highlights(self):
        return self.highlights.filter(is_active=True)

    @property
    def active_cards(self):
        return self.cards.filter(is_active=True)


class CommunityHighlight(OrderedItem):
    community = models.ForeignKey(CommunitySection, on_delete=models.CASCADE, related_name='highlights')
    text = models.CharField('Text', max_length=50)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Highlight word'
        verbose_name_plural = 'Highlight words (gold line at the top, separated by dots)'

    def __str__(self):
        return self.text


class CommunityCard(OrderedItem):
    community = models.ForeignKey(CommunitySection, on_delete=models.CASCADE, related_name='cards')
    icon = models.CharField('Icon', max_length=50, choices=ICON_CHOICES, default='users')
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description', blank=True)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Card'
        verbose_name_plural = 'Cards - numbers 01, 02, 03... are added automatically'

    def __str__(self):
        return self.title
