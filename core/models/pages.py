from django.db import models
from django.urls import reverse

from .base import OrderedItem


class InfoPage(OrderedItem):
    """Simple text pages such as Privacy Policy or Community Guidelines, linked from the footer."""

    title = models.CharField('Title', max_length=150)
    slug = models.SlugField(
        'Web address', max_length=80, unique=True,
        help_text='Last part of the link, e.g. privacy-policy → /privacy-policy/',
    )
    content = models.TextField(
        'Content', blank=True,
        help_text='Leave a blank line between paragraphs. Lines starting with "## " become headings.',
    )
    show_in_footer = models.BooleanField('Link in footer', default=True)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Page (Privacy Policy, Guidelines...)'
        verbose_name_plural = 'Pages (Privacy Policy, Guidelines...)'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('info_page', args=[self.slug])

    @property
    def blocks(self):
        """Content split into headings and paragraphs for the template."""
        result = []
        for chunk in self.content.replace('\r\n', '\n').split('\n\n'):
            chunk = chunk.strip()
            if not chunk:
                continue
            if chunk.startswith('## '):
                result.append({'type': 'heading', 'text': chunk[3:].strip()})
            else:
                result.append({'type': 'paragraph', 'text': chunk})
        return result
