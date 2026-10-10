"""Client request (October 2026): an "Experience MJ Shriram" video block under
the Deepavali Kondattam event, with two Instagram Reel cards, a third Reel as a
small link, and a booking strip. Covers are the Reels' own cover images,
already uploaded to Cloudinary."""

from django.db import migrations

EVENT_TITLE = 'Deepavali Kondattam'

EVENT_TEXT = {
    'reels_heading': 'Experience MJ Shriram',
    'reels_intro': (
        'Watch MJ Shriram in action and get a taste of the music you can enjoy live at '
        'LIT Deepavali Kondattam.'
    ),
    'cta_heading': 'See MJ Shriram Live in London',
    'cta_venue': 'Cranford Suite, TW5 9PD',
    'reels_more_text': 'Watch more MJ Shriram performances on',
    'reels_more_handle': '@londonindiantamils',
    'reels_more_link': 'https://www.instagram.com/londonindiantamils/',
}

COVER_ALT = 'MJ Shriram singing live, Deepavali Kondattam poster'

REELS = [
    (
        'https://www.instagram.com/reel/DdYwb1vt--p/',
        'https://res.cloudinary.com/cikqryjt/image/upload/v1791554561/lit/events/mj_shriram_reel_1_juy2ri.jpg',
    ),
    (
        'https://www.instagram.com/reel/DdqYSe8NOkx/',
        'https://res.cloudinary.com/cikqryjt/image/upload/v1791554562/lit/events/mj_shriram_reel_2_tnyo6l.jpg',
    ),
    (
        'https://www.instagram.com/reel/DePVOApNLDx/',
        'https://res.cloudinary.com/cikqryjt/image/upload/v1791554563/lit/events/mj_shriram_reel_3_b9xut8.jpg',
    ),
]


def add_reels(apps, schema_editor):
    Event = apps.get_model('core', 'Event')
    EventReel = apps.get_model('core', 'EventReel')

    event = Event.objects.filter(title=EVENT_TITLE).order_by('id').first()
    if not event:
        return
    for field, value in EVENT_TEXT.items():
        if not getattr(event, field):
            setattr(event, field, value)
    event.save(update_fields=list(EVENT_TEXT))

    for order, (link, cover) in enumerate(REELS, start=1):
        EventReel.objects.get_or_create(
            event=event, link=link,
            defaults={'order': order, 'cover': cover, 'cover_alt_text': COVER_ALT},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_event_reels'),
    ]

    operations = [
        migrations.RunPython(add_reels, migrations.RunPython.noop),
    ]
