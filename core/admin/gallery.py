from django.contrib import admin

from core.models import GalleryPhoto, GallerySection

from .mixins import OrderedInline, SharedBackgroundAdminMixin, SingletonAdmin, image_preview


class GalleryPhotoInline(OrderedInline):
    model = GalleryPhoto
    fields = ['order', 'image', 'thumbnail', 'size', 'alt_text', 'link', 'is_active']
    readonly_fields = ['thumbnail']
    thumbnail = image_preview('image', label='Preview', height=70)


@admin.register(GallerySection)
class GallerySectionAdmin(SharedBackgroundAdminMixin, SingletonAdmin):
    inlines = [GalleryPhotoInline]
    readonly_fields = ['background_preview', 'updated_at']

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Background', {
            'fields': ['background_image', 'background_preview'],
        }),
        ('Heading', {
            'fields': ['section_label', 'heading_highlight', 'heading'],
        }),
        ('Instagram button', {
            'fields': ['instagram_handle', 'instagram_link'],
        }),
        (None, {'fields': ['updated_at']}),
    ]
