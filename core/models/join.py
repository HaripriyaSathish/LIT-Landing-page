from django.db import models

from .base import (
    JOIN_FORM_HELP, OrderedItem, SharedBackgroundMixin, SingletonModel, image_field, resolve_link,
)


class JoinSection(SharedBackgroundMixin, SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    background_image = image_field(
        'join', 'Section background image', SharedBackgroundMixin.SHARED_BACKGROUND_HELP,
    )
    banner_image = image_field(
        'join', 'Banner photo', 'Wide photo inside the rounded banner, at least 1800x700 px.',
    )
    banner_image_alt_text = models.CharField('Banner photo description', max_length=200, blank=True)

    heading = models.CharField('Heading', max_length=200, default='Join')
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=200, blank=True, default='London Indian Tamils',
        help_text='Shown in the accent colour (italic) after the heading.',
    )
    subheading = models.CharField(
        'Question line', max_length=200, blank=True, default='Tamil-speaking Indian living in the UK?',
    )
    description = models.CharField(
        'Line under the question', max_length=200, blank=True, default='Become part of our growing community.',
    )
    button_text = models.CharField('Button text', max_length=50, blank=True, default='JOIN NOW')
    button_link = models.CharField('Button link', max_length=500, blank=True, help_text=JOIN_FORM_HELP)

    class Meta:
        verbose_name = 'Join Section'
        verbose_name_plural = 'Join Section'

    def __str__(self):
        return 'Join Section'

    @property
    def button(self):
        url, new_tab = resolve_link(self.button_link)
        return {'text': self.button_text, 'url': url, 'new_tab': new_tab}

    @property
    def active_benefits(self):
        return self.benefits.filter(is_active=True)


class JoinBenefit(OrderedItem):
    section = models.ForeignKey(JoinSection, on_delete=models.CASCADE, related_name='benefits')
    text = models.CharField('Text', max_length=60)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Benefit'
        verbose_name_plural = 'Benefits (rounded pills above the button)'

    def __str__(self):
        return self.text
