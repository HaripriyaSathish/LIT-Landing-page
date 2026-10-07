from django.db import models

from .base import OrderedItem, SharedBackgroundMixin, SingletonModel, image_field


class GallerySection(SharedBackgroundMixin, SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    background_image = image_field(
        'gallery', 'Section background image',
        SharedBackgroundMixin.SHARED_BACKGROUND_HELP,
    )
    section_label = models.CharField('Small label above heading', max_length=50, blank=True, default='FOLLOW US')
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=100, blank=True, default='LIT',
        help_text='Shown in gold BEFORE the heading.',
    )
    heading = models.CharField('Heading', max_length=200, default='Community Moments')

    instagram_handle = models.CharField(
        'Instagram name', max_length=100, blank=True, default='@LondonIndianTamils',
        help_text='Button text at the top right. Leave empty to hide the button.',
    )
    instagram_link = models.URLField(
        'Instagram link', max_length=500, blank=True,
        default='https://www.instagram.com/londonindiantamils/',
    )

    class Meta:
        verbose_name = 'Gallery Section'
        verbose_name_plural = 'Gallery Section'

    def __str__(self):
        return 'Gallery Section'

    @property
    def active_photos(self):
        """Photos to show - empty slots without an uploaded image are skipped."""
        return self.photos.filter(is_active=True).exclude(image='')


class GalleryPhoto(OrderedItem):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    SIZE_CHOICES = [
        (SMALL, 'Small (square)'),
        (MEDIUM, 'Medium (square)'),
        (LARGE, 'Large (tall, centre photo)'),
    ]

    gallery = models.ForeignKey(GallerySection, on_delete=models.CASCADE, related_name='photos')
    image = image_field('gallery', 'Photo')
    alt_text = models.CharField('Photo description', max_length=200, blank=True)
    size = models.CharField(
        'Size', max_length=10, choices=SIZE_CHOICES, default=MEDIUM,
        help_text='The design uses: Medium, Small, Large, Small, Medium.',
    )
    link = models.URLField(
        'Link (optional)', max_length=500, blank=True,
        help_text='e.g. the Instagram post. Leave empty to use the Instagram link above.',
    )

    class Meta(OrderedItem.Meta):
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return self.alt_text or f'Photo {self.order}'

    @property
    def url(self):
        return self.link or self.gallery.instagram_link
