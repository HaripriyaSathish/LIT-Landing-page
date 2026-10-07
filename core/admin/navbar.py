from django.contrib import admin

from core.models import Navbar, NavLink

from .mixins import OrderedInline, SingletonAdmin, image_preview


class NavLinkInline(OrderedInline):
    model = NavLink
    fields = ['order', 'label', 'link', 'open_in_new_tab', 'is_active']


@admin.register(Navbar)
class NavbarAdmin(SingletonAdmin):
    inlines = [NavLinkInline]
    readonly_fields = ['logo_preview', 'updated_at']
    logo_preview = image_preview('logo', height=90)

    fieldsets = [
        ('Logo', {
            'fields': ['logo', 'logo_preview', 'logo_alt_text'],
        }),
        ('Name & tagline', {
            'fields': ['brand_name', 'brand_highlight', 'tagline', 'sub_tagline'],
        }),
        ('Button (top right)', {
            'fields': ['show_button', 'button_text', 'button_link'],
        }),
        (None, {'fields': ['updated_at']}),
    ]
