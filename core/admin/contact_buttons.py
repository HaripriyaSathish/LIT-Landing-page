from django.contrib import admin
from django.utils.html import format_html_join

from core.models import FloatingButtons

from .mixins import SingletonAdmin


@admin.register(FloatingButtons)
class FloatingButtonsAdmin(SingletonAdmin):
    readonly_fields = ['showing_now', 'updated_at']

    fieldsets = [
        (None, {
            'fields': ['is_active', 'showing_now'],
            'description': 'Round buttons that float on the side of the page, up to the footer. '
                           'Phone, email and Instagram come from the Contact and Social Media sections '
                           'unless you fill them in here.',
        }),
        ('Call', {'fields': ['show_call', 'phone_number']}),
        ('Email', {'fields': ['show_email', 'email', 'email_subject']}),
        ('Instagram', {'fields': ['show_instagram', 'instagram_link']}),
        ('WhatsApp', {'fields': ['show_whatsapp', 'whatsapp_number', 'whatsapp_message']}),
        (None, {'fields': ['updated_at']}),
    ]

    @admin.display(description='Showing now')
    def showing_now(self, obj):
        buttons = obj.buttons
        if not buttons:
            return 'No buttons - add a phone number or email in the Contact section.'
        return format_html_join(
            ', ', '<a href="{}" target="_blank">{}</a>',
            ((b['url'], b['label']) for b in buttons),
        )
