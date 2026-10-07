from django import forms
from django.contrib import admin

from core.models import SocialLink, SocialSection

from .mixins import OrderedInline, SharedBackgroundAdminMixin, SingletonAdmin


class SocialLinkInline(OrderedInline):
    model = SocialLink
    fields = ['order', 'platform', 'label', 'account_name', 'url', 'is_active', 'show_in_footer', 'footer_order']


class SocialSectionForm(forms.ModelForm):
    class Meta:
        model = SocialSection
        fields = '__all__'
        widgets = {'description': forms.Textarea(attrs={'rows': 2})}


@admin.register(SocialSection)
class SocialSectionAdmin(SharedBackgroundAdminMixin, SingletonAdmin):
    form = SocialSectionForm
    inlines = [SocialLinkInline]
    readonly_fields = ['background_preview', 'updated_at']

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Background', {
            'fields': ['background_image', 'background_preview'],
        }),
        ('Heading & text', {
            'fields': ['section_label', 'heading', 'heading_highlight', 'description'],
        }),
        (None, {'fields': ['updated_at']}),
    ]
