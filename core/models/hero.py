from django.db import models

from .base import JOIN_FORM_HELP, OrderedItem, SingletonModel, image_field, resolve_link


class HeroSection(SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    background_image = image_field(
        'hero', 'Background image', 'Large landscape photo, at least 1920x1080 px.',
    )
    background_image_alt_text = models.CharField('Background image description', max_length=200, blank=True)
    heading = models.CharField('Heading', max_length=200, default='Connecting Indian Tamils Across')
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=200, blank=True, default='London & the UK',
        help_text='Shown in the accent colour (italic) after the heading.',
    )
    description = models.TextField(
        'Main description', blank=True,
        default=(
            'London Indian Tamils (LIT) is a growing community bringing together '
            'Tamil-speaking people of Indian origin living across the UK.'
        ),
    )
    sub_description = models.TextField(
        'Smaller description', blank=True,
        default='Meet people. Make friends. Discover opportunities. Support one another. Celebrate our culture.',
    )
    primary_button_text = models.CharField('Main button text', max_length=50, blank=True, default='JOIN LIT')
    primary_button_link = models.CharField('Main button link', max_length=500, blank=True, help_text=JOIN_FORM_HELP)
    secondary_button_text = models.CharField('Second button text', max_length=50, blank=True, default='VIEW EVENTS')
    secondary_button_link = models.CharField('Second button link', max_length=500, blank=True, default='#events')

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'

    def __str__(self):
        return 'Hero Section'

    @property
    def buttons(self):
        """Buttons that have text, ready for the template."""
        result = []
        for text, link, style in [
            (self.primary_button_text, self.primary_button_link, 'primary'),
            (self.secondary_button_text, self.secondary_button_link, 'secondary'),
        ]:
            if text:
                url, new_tab = resolve_link(link) if style == 'primary' else (link or '#', link.startswith('http'))
                result.append({'text': text, 'url': url, 'new_tab': new_tab, 'style': style})
        return result

    @property
    def active_tags(self):
        return self.tags.filter(is_active=True)


class HeroTag(OrderedItem):
    hero = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name='tags')
    text = models.CharField('Text', max_length=50)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Badge word'
        verbose_name_plural = 'Badge words (shown above the heading, separated by dots)'

    def __str__(self):
        return self.text
