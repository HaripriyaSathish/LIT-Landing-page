from django.db import models

from core.icons import ICON_CHOICES

from .base import OrderedItem, SharedBackgroundMixin, SingletonModel, image_field


def _time(value):
    """6:30 PM style (no leading zero, works on Windows too)."""
    return value.strftime('%I:%M %p').lstrip('0')


class EventsSection(SharedBackgroundMixin, SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    background_image = image_field(
        'events', 'Section background image',
        SharedBackgroundMixin.SHARED_BACKGROUND_HELP,
    )
    section_label = models.CharField('Small label above heading', max_length=50, blank=True, default='EVENTS')
    heading = models.CharField('Heading', max_length=200, default='Meet. Celebrate.')
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=200, blank=True, default='Connect.',
        help_text='Shown in the accent colour (italic) after the heading.',
    )
    description = models.TextField(
        'Description', blank=True,
        default='LIT brings our online community together through real-world experiences.',
    )

    class Meta:
        verbose_name = 'Events Section'
        verbose_name_plural = 'Events Section'

    def __str__(self):
        return 'Events Section'

    @property
    def active_highlights(self):
        return self.highlights.filter(is_active=True)

    @property
    def active_events(self):
        return Event.objects.filter(is_active=True)


class EventsHighlight(OrderedItem):
    section = models.ForeignKey(EventsSection, on_delete=models.CASCADE, related_name='highlights')
    text = models.CharField('Text', max_length=50)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Highlight word'
        verbose_name_plural = 'Highlight words (gold line under the description, separated by dots)'

    def __str__(self):
        return self.text


class Event(OrderedItem):
    badge_text = models.CharField(
        'Badge', max_length=50, blank=True, default='FEATURED EVENT',
        help_text='Small outlined label above the title. Leave empty to hide.',
    )
    title = models.CharField('Event name', max_length=150)
    title_highlight = models.CharField(
        'Highlighted part of name', max_length=50, blank=True,
        help_text='Shown in gold on its own line, e.g. the year.',
    )
    background_image = image_field('events', 'Event background image', 'Landscape photo, at least 1600x800 px.')
    background_image_alt_text = models.CharField('Image description', max_length=200, blank=True)

    featured_photo = image_field(
        'events', 'Artist / featured photo (optional)',
        'e.g. the approved photo of the performer. Shown as a round portrait next to the gold banner.',
    )
    featured_photo_alt_text = models.CharField('Featured photo description', max_length=200, blank=True)

    banner_icon = models.CharField('Banner icon', max_length=50, choices=ICON_CHOICES, blank=True, default='music')
    banner_text = models.CharField(
        'Banner text', max_length=100, blank=True,
        help_text='The big gold strip, e.g. the performer. Leave empty to hide.',
    )

    date = models.DateField('Date')
    start_time = models.TimeField('Start time', null=True, blank=True)
    end_time = models.TimeField('End time', null=True, blank=True)
    venue = models.CharField('Venue / pick-up', max_length=255, blank=True)
    venue_map_link = models.URLField(
        'Venue map link', max_length=500, blank=True,
        help_text='Optional Google Maps link - the venue becomes clickable.',
    )
    ticket_info = models.CharField('Ticket information', max_length=150, blank=True)
    ticket_note = models.CharField(
        'Ticket note (small text)', max_length=150, blank=True,
        help_text='Shown in smaller text after the ticket information, e.g. (food and drinks not included.)',
    )

    button_text = models.CharField('Button text', max_length=50, blank=True, default='BOOK NOW')
    button_link = models.CharField(
        'Booking link', max_length=500, blank=True,
        help_text='Direct Ticket Tailor link for this event. Leave empty to use the main '
                  'event booking link in Site Settings.',
    )

    # Performance video block shown under the event card (only when it has reels)
    reels_heading = models.CharField(
        'Video section heading', max_length=150, blank=True,
        help_text='e.g. Experience MJ Shriram. The block shows when this event has at least one video below.',
    )
    reels_intro = models.TextField('Video section intro', blank=True)
    cta_heading = models.CharField(
        'Booking strip heading', max_length=150, blank=True,
        help_text='Shown above the BOOK NOW button under the videos, e.g. See MJ Shriram Live in London.',
    )
    cta_venue = models.CharField(
        'Booking strip venue (short)', max_length=150, blank=True,
        help_text='Short venue for the booking strip, e.g. Cranford Suite, TW5 9PD. Leave empty to use the venue.',
    )
    reels_more_text = models.CharField(
        'Watch more line - text', max_length=150, blank=True,
        help_text='e.g. Watch more MJ Shriram performances on. Leave empty to hide the line.',
    )
    reels_more_handle = models.CharField('Watch more line - Instagram name', max_length=100, blank=True)
    reels_more_link = models.URLField('Watch more line - link', max_length=500, blank=True)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.title} {self.title_highlight}'.strip()

    @property
    def date_display(self):
        """e.g. Saturday 31 October 2026 | 6:30 PM – 11:00 PM"""
        text = f'{self.date:%A} {self.date.day} {self.date:%B %Y}'
        if self.start_time:
            text += f' | {_time(self.start_time)}'
            if self.end_time:
                text += f' – {_time(self.end_time)}'
        return text

    @property
    def button(self):
        from .site import SiteSettings

        url = self.button_link or SiteSettings.load().booking_url or '#'
        return {'text': self.button_text, 'url': url, 'new_tab': url.startswith(('http://', 'https://'))}

    @property
    def active_features(self):
        return self.features.filter(is_active=True)

    # Two reels are shown as big cards; any others become small links underneath.
    FEATURED_REELS = 2

    @property
    def active_reels(self):
        # filtered in Python so the home page's prefetch is reused
        return [reel for reel in self.reels.all() if reel.is_active]

    @property
    def featured_reels(self):
        return self.active_reels[:self.FEATURED_REELS]

    @property
    def extra_reels(self):
        return self.active_reels[self.FEATURED_REELS:]


class EventReel(OrderedItem):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reels')
    link = models.URLField('Instagram Reel link', max_length=500, help_text='Opens in a new tab.')
    cover = image_field('events', 'Cover image', 'Portrait (9:16) cover of the video, about 360x640 px.')
    cover_alt_text = models.CharField('Cover description', max_length=200, blank=True)
    caption = models.CharField(
        'Caption', max_length=100, blank=True,
        help_text='Optional short line on the card. Extra videos (3rd onwards) use it as the link text.',
    )

    class Meta(OrderedItem.Meta):
        verbose_name = 'Performance video'
        verbose_name_plural = 'Performance videos (first 2 shown as cards, the rest as small links)'

    def __str__(self):
        return self.caption or self.link


class EventFeature(OrderedItem):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='features')
    text = models.CharField('Text', max_length=100)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Feature'
        verbose_name_plural = 'Features (line under the banner, separated by dots)'

    def __str__(self):
        return self.text
