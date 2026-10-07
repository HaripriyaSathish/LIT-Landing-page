from django import forms
from django.contrib import admin

from core.models import HeroSection, HeroTag

from .mixins import OrderedInline, SingletonAdmin, image_preview


class HeroTagInline(OrderedInline):
    model = HeroTag
    fields = ['order', 'text', 'is_active']


class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'sub_description': forms.Textarea(attrs={'rows': 2}),
        }


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    form = HeroSectionForm
    inlines = [HeroTagInline]
    readonly_fields = ['background_preview', 'updated_at']
    background_preview = image_preview('background_image', height=180)

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Background', {
            'fields': ['background_image', 'background_preview', 'background_image_alt_text'],
        }),
        ('Heading & text', {
            'fields': ['heading', 'heading_highlight', 'description', 'sub_description'],
        }),
        ('Buttons', {
            'fields': [
                ('primary_button_text', 'primary_button_link'),
                ('secondary_button_text', 'secondary_button_link'),
            ],
            'description': 'Leave the text empty to hide a button. '
                           'Links can be #section-name (e.g. #events) or a full web address.',
        }),
        (None, {'fields': ['updated_at']}),
    ]
