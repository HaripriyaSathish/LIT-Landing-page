from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from core.models import Footer, SocialSection

from .mixins import SingletonAdmin


@admin.register(Footer)
class FooterAdmin(SingletonAdmin):
    readonly_fields = ['copyright_preview', 'social_icons', 'updated_at']

    fieldsets = [
        ('Name & tagline', {
            'fields': ['brand_name', 'tagline', 'quote'],
        }),
        ('Social media icons', {
            'fields': ['show_social_icons', 'social_icons'],
        }),
        ('Copyright', {
            'fields': ['copyright_text', 'copyright_preview'],
        }),
        ('Designer credit', {
            'fields': ['show_credit', 'credit_text', 'credit_link'],
        }),
        (None, {'fields': ['updated_at']}),
    ]

    @admin.display(description='Shows as')
    def copyright_preview(self, obj):
        return obj.copyright

    @admin.display(description='Icons shown')
    def social_icons(self, obj):
        names = ', '.join(link.get_platform_display() for link in obj.social_links) or 'None'
        url = reverse('admin:core_socialsection_change', args=[SocialSection.load().pk])
        return format_html('{} &nbsp; <a href="{}">Edit social accounts &rarr;</a>', names, url)
