from django import forms
from django.contrib import admin
from django.db import models

from core.models import CommunityCard, CommunityHighlight, CommunitySection

from .mixins import OrderedInline, SharedBackgroundAdminMixin, SingletonAdmin


class CommunityHighlightInline(OrderedInline):
    model = CommunityHighlight
    fields = ['order', 'text', 'is_active']


class CommunityCardInline(OrderedInline):
    model = CommunityCard
    fields = ['order', 'icon', 'title', 'description', 'is_active']
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 50})},
    }


@admin.register(CommunitySection)
class CommunitySectionAdmin(SharedBackgroundAdminMixin, SingletonAdmin):
    inlines = [CommunityHighlightInline, CommunityCardInline]
    readonly_fields = ['background_preview', 'updated_at']

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Background', {
            'fields': ['background_image', 'background_preview'],
        }),
        ('Heading', {
            'fields': ['section_label', 'heading', 'heading_highlight'],
        }),
        (None, {'fields': ['updated_at']}),
    ]
