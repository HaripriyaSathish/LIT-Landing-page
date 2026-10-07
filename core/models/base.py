import re

from django.core.exceptions import ValidationError
from django.db import models

from core.storage import CloudinaryOrLocalStorage


def image_field(folder, verbose_name, help_text=''):
    """An optional image uploaded to Cloudinary (folder lit/<folder>)."""
    return models.ImageField(
        verbose_name,
        upload_to=folder,
        storage=CloudinaryOrLocalStorage(folder),
        max_length=500,
        blank=True,
        help_text=help_text,
    )


JOIN_FORM_HELP = 'Leave empty to open the Join LIT Google Form (set in Site Settings).'


def resolve_link(link):
    """Return (url, opens_new_tab). An empty link means the Join LIT Google Form."""
    if not link:
        from core.models import SiteSettings

        link = SiteSettings.load().join_form_url or '#'
    return link, link.startswith(('http://', 'https://'))


def phone_link(number, country_code='44'):
    """International form of a phone number: '07940 173183' -> '+447940173183'."""
    number = (number or '').strip()
    digits = re.sub(r'\D', '', number)
    if not digits:
        return ''
    if number.startswith('+'):
        return f'+{digits}'
    if digits.startswith('00'):
        return f'+{digits[2:]}'
    if digits.startswith('0'):
        return f'+{country_code}{digits[1:]}'
    return f'+{digits}'


class SharedBackgroundMixin:
    """For sections that reuse the About section's patterned background
    unless they have their own background_image."""

    SHARED_BACKGROUND_HELP = 'Leave empty to use the same background as the About section.'

    @property
    def background(self):
        if self.background_image:
            return self.background_image
        from .about import AboutSection

        return AboutSection.load().background_image


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField('Last updated', auto_now=True)

    class Meta:
        abstract = True


class SingletonModel(TimeStampedModel):
    """A model with exactly one row (pk=1), e.g. a page section."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(f'{self._meta.verbose_name} cannot be deleted.')

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class OrderedItem(TimeStampedModel):
    """A repeatable item (link, card, tag...) shown in display order."""

    order = models.PositiveIntegerField('Display order', default=0, help_text='Lower numbers show first.')
    is_active = models.BooleanField('Show on website', default=True)

    class Meta:
        abstract = True
        ordering = ['order', 'id']
