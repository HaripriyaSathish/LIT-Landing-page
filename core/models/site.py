from django.core.exceptions import ValidationError
from django.db import models

from .base import SingletonModel, image_field


class SiteSettings(SingletonModel):
    # General
    site_title = models.CharField(
        'Website title', max_length=150,
        default='London Indian Tamils (LIT) | Indian Tamil Community in the UK',
        help_text='Shown in the browser tab and search results.',
    )
    meta_description = models.TextField(
        'Search engine description', blank=True,
        help_text='A short summary (about 150 characters) shown by Google.',
    )
    favicon = image_field('site', 'Browser tab icon (favicon)', 'Square image, e.g. 64x64 PNG.')

    # Join LIT
    join_form_url = models.URLField(
        'Join LIT Google Form link', max_length=500, blank=True,
        help_text='Every "JOIN LIT" button opens this form in a new tab. '
                  'Paste the link from Google Forms → Send → link icon.',
    )

    # Event booking
    booking_url = models.URLField(
        'Event booking link (Ticket Tailor)', max_length=500, blank=True,
        default='https://buytickets.at/LIT',
        help_text='Every "BOOK NOW" button opens this, unless the event has its own booking link.',
    )

    # Social sharing & analytics
    og_image = image_field(
        'site', 'Sharing image (WhatsApp / Facebook preview)',
        '1200x630 px. LIT logo + London imagery + name + tagline. Leave empty to use the logo.',
    )
    google_analytics_id = models.CharField(
        'Google Analytics ID', max_length=30, blank=True,
        help_text='Optional, e.g. G-XXXXXXXXXX. Leave empty for no analytics.',
    )

    # Notifications
    notification_email = models.EmailField(
        'Enquiry notification email', blank=True,
        help_text='Form submissions from the website are sent to this address.',
    )

    # Cloudinary
    use_cloudinary = models.BooleanField(
        'Upload images to Cloudinary', default=True,
        help_text='When off (or details are missing), images are stored on this server.',
    )
    cloudinary_cloud_name = models.CharField('Cloud name', max_length=100, blank=True)
    cloudinary_api_key = models.CharField('API key', max_length=100, blank=True)
    cloudinary_api_secret = models.CharField('API secret', max_length=150, blank=True)

    # SMTP
    smtp_host = models.CharField('SMTP server', max_length=150, blank=True, help_text='e.g. smtp.gmail.com')
    smtp_port = models.PositiveIntegerField('SMTP port', default=587, help_text='587 for TLS, 465 for SSL.')
    smtp_username = models.CharField('SMTP username', max_length=150, blank=True)
    smtp_password = models.CharField(
        'SMTP password', max_length=150, blank=True,
        help_text='For Gmail, use an App Password, not your normal password.',
    )
    smtp_use_tls = models.BooleanField('Use TLS', default=True)
    smtp_use_ssl = models.BooleanField('Use SSL', default=False)
    from_email = models.EmailField(
        'Send emails from', blank=True,
        help_text='Usually the same as the SMTP username.',
    )
    from_name = models.CharField('Sender name', max_length=100, default='London Indian Tamils (LIT)')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def clean(self):
        if self.smtp_use_tls and self.smtp_use_ssl:
            raise ValidationError('Choose either TLS or SSL for SMTP, not both.')

    @property
    def cloudinary_is_ready(self):
        return self.use_cloudinary and all(
            [self.cloudinary_cloud_name, self.cloudinary_api_key, self.cloudinary_api_secret]
        )

    @property
    def smtp_is_ready(self):
        return all([self.smtp_host, self.smtp_port, self.from_email or self.smtp_username])

    @property
    def formatted_from_email(self):
        address = self.from_email or self.smtp_username
        return f'{self.from_name} <{address}>' if self.from_name else address
