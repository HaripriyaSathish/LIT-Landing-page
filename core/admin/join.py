from django.contrib import admin

from core.models import JoinBenefit, JoinSection

from .mixins import OrderedInline, SharedBackgroundAdminMixin, SingletonAdmin, image_preview


class JoinBenefitInline(OrderedInline):
    model = JoinBenefit
    fields = ['order', 'text', 'is_active']


@admin.register(JoinSection)
class JoinSectionAdmin(SharedBackgroundAdminMixin, SingletonAdmin):
    inlines = [JoinBenefitInline]
    readonly_fields = ['background_preview', 'banner_preview', 'updated_at']
    banner_preview = image_preview('banner_image', height=160)

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Section background', {
            'fields': ['background_image', 'background_preview'],
        }),
        ('Banner photo', {
            'fields': ['banner_image', 'banner_preview', 'banner_image_alt_text'],
        }),
        ('Heading & text', {
            'fields': ['heading', 'heading_highlight', 'subheading', 'description'],
        }),
        ('Button', {
            'fields': ['button_text', 'button_link'],
        }),
        (None, {'fields': ['updated_at']}),
    ]
