from django import forms
from django.contrib import admin
from django.db import models

from core.models import AboutPillar, AboutSection

from .mixins import OrderedInline, SingletonAdmin, image_preview


class AboutPillarInline(OrderedInline):
    model = AboutPillar
    fields = ['order', 'icon', 'title', 'description', 'is_highlighted', 'is_active']
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
        },
    }


class AboutSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'paragraph_1': forms.Textarea(attrs={'rows': 4}),
            'paragraph_2': forms.Textarea(attrs={'rows': 4}),
        }


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    form = AboutSectionForm
    inlines = [AboutPillarInline]
    readonly_fields = ['background_preview', 'image_preview', 'updated_at']
    background_preview = image_preview('background_image', height=120)
    image_preview = image_preview('image', height=180)

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Background', {
            'fields': ['background_image', 'background_preview'],
        }),
        ('Heading & text', {
            'fields': ['section_label', 'heading', 'heading_highlight', 'paragraph_1', 'paragraph_2'],
        }),
        ('Photo', {
            'fields': ['image', 'image_preview', 'image_alt_text', ('badge_title', 'badge_subtitle')],
        }),
        (None, {'fields': ['updated_at']}),
    ]
