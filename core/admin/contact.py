from django.contrib import admin

from core.models import ContactButton, ContactSection

from .mixins import OrderedInline, SharedBackgroundAdminMixin, SingletonAdmin


class ContactButtonInline(OrderedInline):
    model = ContactButton
    fields = ['order', 'kind', 'label', 'link', 'is_active']


@admin.register(ContactSection)
class ContactSectionAdmin(SharedBackgroundAdminMixin, SingletonAdmin):
    inlines = [ContactButtonInline]
    readonly_fields = ['background_preview', 'updated_at']

    fieldsets = [
        (None, {'fields': ['is_active']}),
        ('Background', {
            'fields': ['background_image', 'background_preview'],
        }),
        ('Heading', {
            'fields': ['section_label', 'heading'],
        }),
        ('Contact details', {
            'fields': ['location', 'location_link', 'email', 'phone'],
            'description': 'The phone and email are also used by the floating Call / Email buttons.',
        }),
        ('Contact person', {
            'fields': ['person_name', 'person_role'],
        }),
        (None, {'fields': ['updated_at']}),
    ]
