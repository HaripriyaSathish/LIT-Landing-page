from django import forms
from django.contrib import admin

from core.models import MessagesSection, SupportMessage

from .mixins import SharedBackgroundAdminMixin, SingletonAdmin, image_preview


class SupportMessageInline(admin.StackedInline):
    model = SupportMessage
    extra = 0
    ordering = ['order', 'id']
    readonly_fields = ['photo_preview']
    photo_preview = image_preview('photo', height=120)
    fields = [
        ('order', 'is_active'),
        ('photo', 'photo_preview'),
        ('name', 'role'),
        'status_text',
        ('button_text', 'video_link'),
    ]


class MessagesSectionForm(forms.ModelForm):
    class Meta:
        model = MessagesSection
        fields = '__all__'
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


@admin.register(MessagesSection)
class MessagesSectionAdmin(SharedBackgroundAdminMixin, SingletonAdmin):
    form = MessagesSectionForm
    inlines = [SupportMessageInline]
    readonly_fields = ['background_preview', 'updated_at']

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Background', {
            'fields': ['background_image', 'background_preview'],
        }),
        ('Heading & text', {
            'fields': ['section_label', 'heading', 'heading_highlight', 'description'],
        }),
        ('Follow line (under the cards)', {
            'fields': ['follow_text_before', 'follow_handle', 'follow_text_after', 'follow_link'],
        }),
        (None, {'fields': ['updated_at']}),
    ]
