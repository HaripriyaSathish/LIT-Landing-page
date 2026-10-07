from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from core.models import (
    AboutSection, CommunitySection, ContactSection, Event, EventFeature, EventsSection,
    FloatingButtons, Footer, GallerySection, HeroSection, InfoPage, JoinSection, MessagesSection,
    Navbar, SiteSettings, SocialSection,
)


def _common_context():
    return {
        'site': SiteSettings.load(),
        'navbar': Navbar.load(),
        'footer': Footer.load(),
    }


def home(request):
    events = Event.objects.filter(is_active=True).prefetch_related(
        Prefetch('features', queryset=EventFeature.objects.filter(is_active=True)),
    )
    context = {
        **_common_context(),
        'hero': HeroSection.load(),
        'about': AboutSection.load(),
        'community': CommunitySection.load(),
        'events_section': EventsSection.load(),
        'events': events,
        'gallery': GallerySection.load(),
        'messages_section': MessagesSection.load(),
        'join': JoinSection.load(),
        'social': SocialSection.load(),
        'contact': ContactSection.load(),
        'floating': FloatingButtons.load(),
    }
    return render(request, 'core/home.html', context)


def info_page(request, slug):
    page = get_object_or_404(InfoPage, slug=slug, is_active=True)
    return render(request, 'core/info_page.html', {**_common_context(), 'page': page})
