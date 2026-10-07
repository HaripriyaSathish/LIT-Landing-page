from urllib.parse import quote

from django.db import models

from .base import SingletonModel, phone_link

SAME_AS_CONTACT = 'Leave empty to use the one in the Contact section.'


class FloatingButtons(SingletonModel):
    """Call / Email / Instagram (/ WhatsApp) buttons that float on the side of the page."""

    is_active = models.BooleanField('Show floating buttons', default=True)

    show_call = models.BooleanField('Show call button', default=True)
    phone_number = models.CharField('Phone number', max_length=30, blank=True, help_text=SAME_AS_CONTACT)

    show_email = models.BooleanField('Show email button', default=True)
    email = models.EmailField('Email address', blank=True, help_text=SAME_AS_CONTACT)
    email_subject = models.CharField(
        'Email subject', max_length=150, blank=True, default='Enquiry from LIT website',
    )

    show_instagram = models.BooleanField('Show Instagram button', default=True)
    instagram_link = models.URLField(
        'Instagram link', max_length=500, blank=True,
        help_text='Leave empty to use the Instagram account in the Social Media section.',
    )

    show_whatsapp = models.BooleanField('Show WhatsApp button', default=False)
    whatsapp_number = models.CharField(
        'WhatsApp number', max_length=30, blank=True,
        help_text='Leave empty to use the Contact section phone number.',
    )
    whatsapp_message = models.CharField(
        'WhatsApp starting message', max_length=300, blank=True,
        default='Hi LIT, I would like to know more about London Indian Tamils.',
        help_text='Pre-filled in the chat when someone taps the button.',
    )

    class Meta:
        verbose_name = 'Floating Contact Buttons'
        verbose_name_plural = 'Floating Contact Buttons'

    def __str__(self):
        return 'Floating Contact Buttons'

    @property
    def _contact(self):
        from .contact import ContactSection

        return ContactSection.load()

    @property
    def call_url(self):
        number = self.phone_number or self._contact.phone
        return f'tel:{phone_link(number)}' if self.show_call and number else ''

    @property
    def email_url(self):
        address = self.email or self._contact.email
        if not (self.show_email and address):
            return ''
        subject = f'?subject={quote(self.email_subject)}' if self.email_subject else ''
        return f'mailto:{address}{subject}'

    @property
    def instagram_url(self):
        from .contact import social_url

        return (self.instagram_link or social_url('instagram')) if self.show_instagram else ''

    @property
    def whatsapp_url(self):
        number = self.whatsapp_number or self._contact.phone
        if not (self.show_whatsapp and number):
            return ''
        text = f'?text={quote(self.whatsapp_message)}' if self.whatsapp_message else ''
        return f'https://wa.me/{phone_link(number).lstrip("+")}{text}'

    @property
    def buttons(self):
        """Buttons to show, in order, ready for the template."""
        if not self.is_active:
            return []
        items = [
            ('call', 'Call us', 'phone', self.call_url),
            ('email', 'Email us', 'mail', self.email_url),
            ('instagram', 'Instagram', 'instagram', self.instagram_url),
            ('whatsapp', 'WhatsApp us', 'message-circle', self.whatsapp_url),
        ]
        return [
            {'type': kind, 'label': label, 'icon': icon, 'url': url}
            for kind, label, icon, url in items if url
        ]
