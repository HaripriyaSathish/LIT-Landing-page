from django.db import models

from .base import OrderedItem, SharedBackgroundMixin, SingletonModel, image_field, phone_link


class ContactSection(SharedBackgroundMixin, SingletonModel):
    """Contact card. Its phone and email are also used by the floating buttons."""

    is_active = models.BooleanField('Show this section', default=True)
    background_image = image_field(
        'contact', 'Section background image', SharedBackgroundMixin.SHARED_BACKGROUND_HELP,
    )
    section_label = models.CharField('Small label above heading', max_length=50, blank=True, default='CONTACT')
    heading = models.CharField('Heading', max_length=200, default='London Indian Tamils')

    location = models.CharField('Location', max_length=200, blank=True, default='London, United Kingdom')
    location_link = models.URLField(
        'Location map link', max_length=500, blank=True,
        help_text='Optional Google Maps link - the location becomes clickable.',
    )
    email = models.EmailField('Email', blank=True)
    phone = models.CharField(
        'Phone', max_length=30, blank=True,
        help_text='Shown exactly as typed, e.g. 07940 173183. UK numbers starting with 0 are dialled as +44.',
    )

    person_name = models.CharField('Contact person', max_length=100, blank=True)
    person_role = models.CharField('Contact person role', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Contact Section'
        verbose_name_plural = 'Contact Section'

    def __str__(self):
        return 'Contact Section'

    @property
    def phone_url(self):
        return f'tel:{phone_link(self.phone)}' if self.phone else ''

    @property
    def email_url(self):
        return f'mailto:{self.email}' if self.email else ''

    @property
    def active_buttons(self):
        return self.buttons.filter(is_active=True)


def social_url(platform):
    """Link of the active social account for a platform (from the Social Media section)."""
    from .social import SocialLink

    account = SocialLink.objects.filter(platform=platform, is_active=True).exclude(url='').first()
    return account.url if account else ''


class ContactButton(OrderedItem):
    KIND_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('youtube', 'YouTube'),
        ('link', 'Other link'),
    ]

    section = models.ForeignKey(ContactSection, on_delete=models.CASCADE, related_name='buttons')
    kind = models.CharField('Type', max_length=20, choices=KIND_CHOICES, help_text='Sets the icon.')
    label = models.CharField('Button text', max_length=50)
    link = models.CharField(
        'Link', max_length=500, blank=True,
        help_text='Leave empty: Call/Email use the phone and email above; '
                  'social buttons use the Social Media section accounts.',
    )

    class Meta(OrderedItem.Meta):
        verbose_name = 'Button'
        verbose_name_plural = 'Buttons'

    ICONS = {
        'call': 'phone', 'email': 'mail', 'instagram': 'instagram', 'facebook': 'facebook',
        'whatsapp': 'message-circle', 'youtube': 'youtube', 'link': 'link',
    }

    def __str__(self):
        return self.label

    @property
    def icon(self):
        return self.ICONS.get(self.kind, 'link')

    @property
    def url(self):
        if self.link:
            return self.link
        if self.kind == 'call':
            return self.section.phone_url
        if self.kind == 'email':
            return self.section.email_url
        return social_url(self.kind)
