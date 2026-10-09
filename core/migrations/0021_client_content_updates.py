"""Client content changes (October 2026): new menu order with Founder and
Voices, updated Young Adults card text, support-message clean-up with the
original Instagram video covers, and a London landmark hero photo."""

from django.db import migrations

NAV_LINKS = [
    ('About', '#about'),
    ('Founder', '#founder'),
    ('Community', '#community'),
    ('Events', '#events'),
    ('Voices', '#messages'),
    ('Join LIT', '#join'),
    ('Contact', '#contact'),
]

OLD_YOUNG_ADULTS = 'A space for the next generation to connect.'
NEW_YOUNG_ADULTS = 'Respectful discussion on UK, Indian and Tamil-related politics and current affairs.'

VIDEO_LINKS = {
    'Srinivas': 'https://www.instagram.com/reel/Db-Z4MnNmfn/',
    'Unni Krishnan': 'https://www.instagram.com/reel/DcU0owEChJ-/',
    'Gopinath': 'https://www.instagram.com/reel/Dcf0wGJtzfm/',
    'Dushyanth Sridhar': 'https://www.instagram.com/reel/DdBrOLMNiJQ/',
}

# Cover image of each Instagram video, already uploaded to Cloudinary
VIDEO_COVERS = {
    'Srinivas': 'https://res.cloudinary.com/cikqryjt/image/upload/v1791520013/lit/messages/srinivas_sxu3jt.jpg',
    'Unni Krishnan': 'https://res.cloudinary.com/cikqryjt/image/upload/v1791520014/lit/messages/unni_krishnan_xkffb2.jpg',
    'Gopinath': 'https://res.cloudinary.com/cikqryjt/image/upload/v1791520016/lit/messages/gopinath_s6rta6.jpg',
    'Dushyanth Sridhar': (
        'https://res.cloudinary.com/cikqryjt/image/upload/v1791520017/lit/messages/dushyanth_sridhar_khixw4.jpg'
    ),
}

HERO_IMAGE = 'https://res.cloudinary.com/cikqryjt/image/upload/v1791520443/lit/hero/big_wMez_KLY3lw_pb3uqz.jpg'
HERO_IMAGE_ALT = 'Tower Bridge, London, under a bright blue sky'


def apply_updates(apps, schema_editor):
    Navbar = apps.get_model('core', 'Navbar')
    NavLink = apps.get_model('core', 'NavLink')
    CommunityCard = apps.get_model('core', 'CommunityCard')
    SupportMessage = apps.get_model('core', 'SupportMessage')
    HeroSection = apps.get_model('core', 'HeroSection')

    navbar = Navbar.objects.filter(pk=1).first()
    if navbar:
        wanted = {link for _, link in NAV_LINKS}
        for extra in NavLink.objects.filter(navbar=navbar).exclude(link__in=wanted):
            extra.order += 100  # keep any custom links, after the main menu
            extra.save(update_fields=['order'])
        for order, (label, link) in enumerate(NAV_LINKS, start=1):
            item = NavLink.objects.filter(navbar=navbar, link=link).first()
            if item:
                item.label, item.order, item.is_active = label, order, True
                item.save(update_fields=['label', 'order', 'is_active'])
            else:
                NavLink.objects.create(navbar=navbar, label=label, link=link, order=order)

    CommunityCard.objects.filter(description=OLD_YOUNG_ADULTS).update(description=NEW_YOUNG_ADULTS)

    SupportMessage.objects.filter(status_text__iexact='Message coming soon').update(status_text='')
    for name, url in VIDEO_LINKS.items():
        SupportMessage.objects.filter(name=name, video_link='').update(video_link=url)
    for name, cover in VIDEO_COVERS.items():
        SupportMessage.objects.filter(name=name).update(photo=cover)

    HeroSection.objects.filter(pk=1).update(background_image=HERO_IMAGE, background_image_alt_text=HERO_IMAGE_ALT)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_support_message_defaults'),
    ]

    operations = [
        migrations.RunPython(apply_updates, migrations.RunPython.noop),
    ]
