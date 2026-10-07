"""
Fill the admin with the website content from the Figma design.

    python manage.py seed_data          # only fills sections that are still empty
    python manage.py seed_data --force  # overwrite text with the original design content

Images are not seeded - upload them in the admin.
"""
import os
from datetime import date, time

from django.core.management.base import BaseCommand
from django.db import transaction

from core.management.pages_content import COMMUNITY_GUIDELINES, PRIVACY_POLICY
from core.models import (
    AboutPillar, AboutSection, CommunityCard, CommunityHighlight, CommunitySection,
    ContactButton, ContactSection, Event, EventFeature, EventsHighlight, EventsSection,
    FloatingButtons, Footer, GalleryPhoto, GallerySection, HeroSection, HeroTag, InfoPage,
    JoinBenefit, JoinSection, MessagesSection, Navbar, NavLink, SiteSettings,
    SocialLink, SocialSection, SupportMessage,
)

SITE_SETTINGS = {
    'site_title': 'London Indian Tamils (LIT) | Indian Tamil Community in the UK',
    'booking_url': 'https://buytickets.at/LIT',
    'join_form_url': 'https://forms.gle/wr2wboJoV3MhghLy6',
    'meta_description': (
        'London Indian Tamils (LIT) connects Tamil-speaking Indians across London and the UK through '
        'community, careers, business, sports, social activities and events.'
    ),
    'from_name': 'London Indian Tamils (LIT)',
}

NAVBAR = {
    'logo_alt_text': 'London Indian Tamils (LIT) logo',
    'brand_name': 'London Indian Tamils',
    'brand_highlight': '(LIT)',
    'tagline': 'CONNECT • SUPPORT • CELEBRATE',
    'sub_tagline': 'India in our heart. London in our home. Tamil in our identity.',
    'show_button': True,
    'button_text': 'JOIN LIT',
    'button_link': '',  # empty = Join LIT Google Form from Site Settings
}

NAV_LINKS = [
    ('About', '#about'),
    ('Community', '#community'),
    ('Events', '#events'),
    ('Join LIT', '#join'),
    ('Contact', '#contact'),
]

HERO = {
    'is_active': True,
    'background_image_alt_text': '',
    'heading': 'Connecting Indian Tamils Across',
    'heading_highlight': 'London & the UK',
    'description': (
        'London Indian Tamils (LIT) is a growing community bringing together '
        'Tamil-speaking people of Indian origin living across the UK.'
    ),
    'sub_description': 'Meet people. Make friends. Discover opportunities. Support one another. Celebrate our culture.',
    'primary_button_text': 'JOIN LIT',
    'primary_button_link': '',  # empty = Join LIT Google Form from Site Settings
    'secondary_button_text': 'VIEW EVENTS',
    'secondary_button_link': '#events',
}

HERO_TAGS = ['LONDON', 'தமிழ்', 'INDIA', 'UK']

ABOUT = {
    'is_active': True,
    'section_label': 'ABOUT LIT',
    'heading': 'More Than a WhatsApp Group.',
    'heading_highlight': 'A Community.',
    'paragraph_1': (
        'London Indian Tamils (LIT) is a growing community bringing together Tamil-speaking people '
        'of Indian origin living across the UK — a place to meet people, make friends, discover '
        'opportunities, support one another and celebrate our culture.'
    ),
    'paragraph_2': (
        'A place to build friendships, share opportunities, support businesses and careers, celebrate '
        'our culture and participate in social, educational, sporting and community activities.'
    ),
    'image_alt_text': '',
    'badge_title': 'தமிழ்',
    'badge_subtitle': 'ONE COMMUNITY',
}

ABOUT_PILLARS = [
    {
        'icon': 'users',
        'title': 'Connect',
        'description': 'Meet people, make friends and build personal and professional connections.',
    },
    {
        'icon': 'heart-handshake',
        'title': 'Support',
        'description': 'Share opportunities, support careers and businesses and help one another.',
    },
    {
        'icon': 'sparkles',
        'title': 'Celebrate',
        'description': (
            'Celebrate our Tamil language, Indian roots, culture, festivals, music, food and traditions.'
        ),
    },
]

COMMUNITY = {
    'is_active': True,
    'section_label': 'OUR COMMUNITY',
    'heading': "There's Something",
    'heading_highlight': 'for Everyone',
}

COMMUNITY_HIGHLIGHTS = [
    'A growing UK community', 'Social', 'Careers', 'Business',
    'Sports', 'Families', 'Young Adults', 'Events',
]

COMMUNITY_CARDS = [
    ('users', 'Social', 'Meet-ups, friendships and good times together.'),
    ('briefcase', 'Jobs & Careers', 'Openings, referrals and career guidance.'),
    ('store', 'Business & Networking',
     'Connect, collaborate and support businesses and professionals within our community.'),
    ('shopping-bag', 'Marketplace', 'Buy, sell and recommend within the community.'),
    ('party-popper', 'Young Adults – 18 to 30', 'A space for the next generation to connect.'),
    ('trophy', 'Sports & Fitness', 'Cricket, badminton, runs and staying active.'),
    ('graduation-cap', 'Kids & Education', 'Tamil learning, schools and family support.'),
    ('calendar-heart', 'Events & Activities', 'Festivals, trips, music and celebrations.'),
]

EVENTS = {
    'is_active': True,
    'section_label': 'EVENTS',
    'heading': 'Meet. Celebrate.',
    'heading_highlight': 'Connect.',
    'description': 'LIT brings our online community together through real-world experiences.',
}

EVENTS_HIGHLIGHTS = [
    'Social Meet-ups', 'Live Music', 'Cultural Events', 'Open Mic', 'Family Activities',
    'Sports', 'Networking', 'Day Trips', 'Festivals',
]

EVENT_LIST = [
    {
        'event': {
            'badge_text': 'FEATURED EVENT',
            'title': 'Deepavali Kondattam',
            'title_highlight': '2026',
            'banner_icon': 'music',
            'banner_text': 'LIVE WITH MJ SHRIRAM',
            'date': date(2026, 10, 31),
            'start_time': time(18, 30),
            'end_time': time(23, 0),
            'venue': 'Cranford Suite, Cranford Community College, TW5 9PD',
            'ticket_info': 'Tickets from £22.50 including 3-course dinner',
            'button_text': 'BOOK NOW',
            'button_link': '',  # empty = event booking link (Ticket Tailor) from Site Settings
        },
        'features': ['Live Music', '3-Course Dinner', 'Family Entertainment', 'Deepavali Celebration'],
    },
    {
        'event': {
            'badge_text': 'FEATURED EVENT',
            'title': 'Christmas Market: Bath Day Trip',
            'title_highlight': '2026',
            'banner_icon': '',
            'banner_text': '',
            'date': date(2026, 12, 12),
            'start_time': None,
            'end_time': None,
            'venue': 'Pick-up 9:00 AM at Hillingdon Station and 9:30 AM at M4 Reading Services Westbound',
            'ticket_info': '£15 per person including children',
            'ticket_note': '(food and drinks not included.)',
            'button_text': 'BOOK NOW',
            'button_link': '',  # empty = event booking link (Ticket Tailor) from Site Settings
        },
        'features': [],
    },
]

GALLERY = {
    'is_active': True,
    'section_label': 'FOLLOW US',
    'heading_highlight': 'LIT',
    'heading': 'Community Moments',
    'instagram_handle': '@LondonIndianTamils',
    'instagram_link': 'https://www.instagram.com/londonindiantamils/',
}

# Empty photo slots in the design's size pattern - upload the photos in the admin.
GALLERY_PHOTO_SIZES = ['medium', 'small', 'large', 'small', 'medium']

MESSAGES = {
    'is_active': True,
    'section_label': 'VOICES OF SUPPORT',
    'heading': 'Messages to the',
    'heading_highlight': 'LIT Community',
    'description': (
        'We’re grateful to have received special messages of support and encouragement for '
        'London Indian Tamils from respected personalities from the Tamil community.'
    ),
    'follow_text_before': 'Follow',
    'follow_handle': '@londonindiantamils',
    'follow_text_after': 'for more community stories, messages and updates.',
    'follow_link': 'https://www.instagram.com/londonindiantamils/',
}

SUPPORT_MESSAGES = [
    ('Srinivas', 'Singer'),
    ('Unni Krishnan', 'Singer'),
    ('Gopinath', 'Neeya Naana'),
    ('Dushyanth Sridhar', 'Speaker & Author'),
]

JOIN = {
    'is_active': True,
    'heading': 'Join',
    'heading_highlight': 'London Indian Tamils',
    'subheading': 'Tamil-speaking Indian living in the UK?',
    'description': 'Become part of our growing community.',
    'button_text': 'JOIN NOW',
    'button_link': '',  # empty = Join LIT Google Form from Site Settings
}

JOIN_BENEFITS = [
    'Connect with people', 'Make friends', 'Find opportunities',
    'Support businesses', 'Attend events', 'Celebrate together',
]

SOCIAL = {
    'is_active': True,
    'section_label': 'SOCIAL MEDIA',
    'heading': 'Stay Connected',
    'heading_highlight': 'With LIT',
    'description': 'Follow us for community news, event announcements, photos, videos and activities.',
}

SOCIAL_LINKS = [
    {
        'platform': 'instagram',
        'label': 'INSTAGRAM',
        'account_name': '@londonindiantamils',
        'url': 'https://www.instagram.com/londonindiantamils/',
        'show_in_footer': True,
        'footer_order': 2,
    },
    {
        'platform': 'facebook',
        'label': 'FACEBOOK',
        'account_name': 'London Indian Tamils',
        'url': 'https://www.facebook.com/profile.php?id=61593266637975',
        'show_in_footer': True,
        'footer_order': 1,
    },
]

CONTACT = {
    'is_active': True,
    'section_label': 'CONTACT',
    'heading': 'London Indian Tamils',
    'location': 'London, United Kingdom',
    'email': 'londonindiantamils@gmail.com',
    'phone': '07940 173183',
    'person_name': 'Sathish Duraisamy',
    'person_role': 'Founder & Director',
}

# Empty links = use the contact details / Social Media accounts.
CONTACT_BUTTONS = [
    {'kind': 'call', 'label': 'CALL'},
    {'kind': 'email', 'label': 'EMAIL'},
    {'kind': 'instagram', 'label': 'INSTAGRAM'},
    {'kind': 'facebook', 'label': 'FACEBOOK'},
]

FOOTER = {
    'brand_name': 'LONDON INDIAN TAMILS',
    'tagline': 'CONNECT • SUPPORT • CELEBRATE',
    'quote': 'India in our heart. London in our home. Tamil in our identity.',
    'show_social_icons': True,
    'copyright_text': 'London Indian Tamils. All Rights Reserved.',
}

# Phone and email come from the Contact section; Instagram from the Social Media section.
FLOATING_BUTTONS = {
    'is_active': True,
    'show_call': True,
    'phone_number': '',
    'show_email': True,
    'email': '',
    'email_subject': 'Enquiry from LIT website',
    'show_instagram': True,
    'instagram_link': '',
    'show_whatsapp': False,
    'whatsapp_message': 'Hi LIT, I would like to know more about London Indian Tamils.',
}


class Command(BaseCommand):
    help = 'Seed the website content shown in the Figma design.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Overwrite existing content with the original design content.',
        )

    @transaction.atomic
    def handle(self, *args, force=False, **options):
        self.force = force
        self.seed_site_settings()
        self.seed_singleton(Navbar, NAVBAR, 'links', NavLink, 'navbar',
                            [{'label': label, 'link': link} for label, link in NAV_LINKS])
        self.seed_singleton(HeroSection, HERO, 'tags', HeroTag, 'hero',
                            [{'text': text} for text in HERO_TAGS])
        self.seed_singleton(AboutSection, ABOUT, 'pillars', AboutPillar, 'about', ABOUT_PILLARS)
        community = self.seed_singleton(
            CommunitySection, COMMUNITY, 'highlights', CommunityHighlight, 'community',
            [{'text': text} for text in COMMUNITY_HIGHLIGHTS],
        )
        self.seed_items(community, 'cards', CommunityCard, 'community', [
            {'icon': icon, 'title': title, 'description': description}
            for icon, title, description in COMMUNITY_CARDS
        ])
        self.seed_singleton(
            EventsSection, EVENTS, 'highlights', EventsHighlight, 'section',
            [{'text': text} for text in EVENTS_HIGHLIGHTS],
        )
        self.seed_events()
        self.seed_singleton(
            GallerySection, GALLERY, 'photos', GalleryPhoto, 'gallery',
            [{'size': size} for size in GALLERY_PHOTO_SIZES],
        )
        self.seed_singleton(
            MessagesSection, MESSAGES, 'messages', SupportMessage, 'section',
            [{'name': name, 'role': role, 'status_text': 'Message coming soon', 'button_text': 'Watch Message'}
             for name, role in SUPPORT_MESSAGES],
        )
        self.seed_singleton(
            JoinSection, JOIN, 'benefits', JoinBenefit, 'section', [{'text': text} for text in JOIN_BENEFITS],
        )
        self.seed_singleton(SocialSection, SOCIAL, 'links', SocialLink, 'section', SOCIAL_LINKS)
        self.seed_singleton(ContactSection, CONTACT, 'buttons', ContactButton, 'section', CONTACT_BUTTONS)
        self.seed_singleton(Footer, FOOTER)
        self.seed_singleton(FloatingButtons, FLOATING_BUTTONS)
        self.seed_pages()
        self.stdout.write(self.style.SUCCESS('Seed data loaded.'))

    def seed_pages(self):
        pages = [
            ('Privacy Policy', 'privacy-policy', PRIVACY_POLICY),
            ('Community Guidelines', 'community-guidelines', COMMUNITY_GUIDELINES),
        ]
        for order, (title, slug, content) in enumerate(pages, start=1):
            page, created = InfoPage.objects.get_or_create(
                slug=slug, defaults={'title': title, 'content': content, 'order': order},
            )
            if self.force and not created:
                page.title, page.content = title, content
                page.save()
        self.stdout.write('  Footer pages: checked')

    def seed_events(self):
        """Add each design event by name; existing events are kept unless --force."""
        if self.force:
            Event.objects.all().delete()
        added = 0
        for index, item in enumerate(EVENT_LIST, start=1):
            data = item['event']
            event, created = Event.objects.get_or_create(
                title=data['title'], defaults={**data, 'order': index},
            )
            if created:
                added += 1
                self.seed_items(event, 'features', EventFeature, 'event', [{'text': t} for t in item['features']])
        self.stdout.write(f'  Events: {added} added, {len(EVENT_LIST) - added} already there')

    def seed_site_settings(self):
        site, created = SiteSettings.objects.get_or_create(pk=1, defaults=SITE_SETTINGS)
        if self.force and not created:
            for field, value in SITE_SETTINGS.items():
                setattr(site, field, value)

        # One-time move of Cloudinary keys from .env into the admin.
        env_keys = {
            'cloudinary_cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', ''),
            'cloudinary_api_key': os.getenv('CLOUDINARY_API_KEY', ''),
            'cloudinary_api_secret': os.getenv('CLOUDINARY_API_SECRET', ''),
        }
        if not site.cloudinary_is_ready and all(env_keys.values()):
            for field, value in env_keys.items():
                setattr(site, field, value)
            self.stdout.write('  Site Settings: copied Cloudinary keys from .env')

        site.save()
        self.stdout.write(f'  Site Settings: {"created" if created else "checked"}')

    def seed_singleton(self, model, data, related_name=None, item_model=None, fk_name=None, items=()):
        obj, created = model.objects.get_or_create(pk=1, defaults=data)
        if self.force and not created:
            for field, value in data.items():
                setattr(obj, field, value)
            obj.save()

        if related_name:
            self.seed_items(obj, related_name, item_model, fk_name, items)

        status = 'created' if created else ('overwritten' if self.force else 'already had content, kept')
        self.stdout.write(f'  {model._meta.verbose_name}: {status}')
        return obj

    def seed_items(self, parent, related_name, item_model, fk_name, items):
        related = getattr(parent, related_name)
        if self.force:
            related.all().delete()
        if not related.exists():
            item_model.objects.bulk_create([
                item_model(**{fk_name: parent}, order=index, **item)
                for index, item in enumerate(items, start=1)
            ])
