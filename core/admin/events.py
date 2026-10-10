from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from core.models import Event, EventFeature, EventReel, EventsHighlight, EventsSection

from .mixins import OrderedInline, SharedBackgroundAdminMixin, SingletonAdmin, image_preview


class EventsHighlightInline(OrderedInline):
    model = EventsHighlight
    fields = ['order', 'text', 'is_active']


@admin.register(EventsSection)
class EventsSectionAdmin(SharedBackgroundAdminMixin, SingletonAdmin):
    inlines = [EventsHighlightInline]
    readonly_fields = ['background_preview', 'manage_events', 'updated_at']

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Background', {
            'fields': ['background_image', 'background_preview'],
        }),
        ('Heading & text', {
            'fields': ['section_label', 'heading', 'heading_highlight', 'description'],
        }),
        ('Events', {'fields': ['manage_events']}),
        (None, {'fields': ['updated_at']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'description': forms.Textarea(attrs={'rows': 2})}
        return super().get_form(request, obj, **kwargs)


    @admin.display(description='Event cards')
    def manage_events(self, obj):
        return format_html(
            '{} event(s) shown. <a href="{}">Add or edit events &rarr;</a>',
            obj.active_events.count(), reverse('admin:core_event_changelist'),
        )


class EventFeatureInline(OrderedInline):
    model = EventFeature
    fields = ['order', 'text', 'is_active']


class EventReelInline(admin.StackedInline):
    model = EventReel
    extra = 0
    ordering = ['order', 'id']
    readonly_fields = ['cover_preview']
    cover_preview = image_preview('cover', height=160)
    fields = [
        ('order', 'is_active'),
        'link',
        ('cover', 'cover_preview'),
        ('cover_alt_text', 'caption'),
    ]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventFeatureInline, EventReelInline]
    list_display = ['__str__', 'date', 'venue', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'venue']
    readonly_fields = ['background_preview', 'featured_preview', 'updated_at']
    background_preview = image_preview('background_image', height=160)
    featured_preview = image_preview('featured_photo', height=120)

    fieldsets = [
        (None, {'fields': ['is_active', 'order']}),
        ('Title', {
            'fields': ['badge_text', 'title', 'title_highlight'],
        }),
        ('Background', {
            'fields': ['background_image', 'background_preview', 'background_image_alt_text'],
        }),
        ('Gold banner & artist photo (optional)', {
            'fields': ['banner_icon', 'banner_text', 'featured_photo', 'featured_preview', 'featured_photo_alt_text'],
            'description': 'Leave the banner text empty to hide the banner.',
        }),
        ('Details', {
            'fields': ['date', ('start_time', 'end_time'), 'venue', 'venue_map_link', 'ticket_info', 'ticket_note'],
        }),
        ('Button', {
            'fields': ['button_text', 'button_link'],
        }),
        ('Performance videos block (optional, under the event card)', {
            'fields': [
                'reels_heading', 'reels_intro', 'cta_heading', 'cta_venue',
                'reels_more_text', ('reels_more_handle', 'reels_more_link'),
            ],
            'description': 'Shown when this event has at least one performance video (added at the bottom '
                           'of this page). The booking strip reuses the date, ticket information and button above.',
        }),
        (None, {'fields': ['updated_at']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'reels_intro': forms.Textarea(attrs={'rows': 2})}
        return super().get_form(request, obj, **kwargs)
