from django.contrib import admin

from . import about, community, contact, contact_buttons, events, footer, gallery, hero, join, messages, navbar, pages, site, social  # noqa: F401  (registers the admin classes)

admin.site.site_header = 'London Indian Tamils (LIT) - Admin'
admin.site.site_title = 'LIT Admin'
admin.site.index_title = 'Manage your website'
