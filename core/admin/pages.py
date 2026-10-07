from django.contrib import admin
from django.utils.html import format_html

from core.models import InfoPage


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_link', 'order', 'show_in_footer', 'is_active']
    list_editable = ['order', 'show_in_footer', 'is_active']
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = ['updated_at']
    fields = ['title', 'slug', 'content', ('order', 'show_in_footer', 'is_active'), 'updated_at']

    @admin.display(description='Link')
    def page_link(self, obj):
        url = obj.get_absolute_url()
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)
