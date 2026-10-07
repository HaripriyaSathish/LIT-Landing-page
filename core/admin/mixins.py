from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe


def image_preview(field_name, label='Preview', height=120):
    """Build a read-only admin field that shows a thumbnail of an image field."""

    @admin.display(description=label)
    def preview(self, obj):
        image = getattr(obj, field_name, None)
        if not image:
            return 'No image uploaded yet.'
        return format_html(
            '<a href="{0}" target="_blank"><img src="{0}" style="max-height:{1}px;max-width:100%;'
            'border-radius:6px;border:1px solid #ddd;padding:2px;background:#f8f8f8"></a>',
            image.url, height,
        )

    return preview


class SingletonAdmin(admin.ModelAdmin):
    """Admin for a one-record section: opens the edit form directly, no add/delete."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        opts = self.model._meta
        return redirect(reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[obj.pk]))

    def response_change(self, request, obj):
        # "Save" keeps you on the same page instead of an (empty) list page.
        if '_continue' not in request.POST and '_addanother' not in request.POST:
            request.POST = request.POST.copy()
            request.POST['_continue'] = '1'
        return super().response_change(request, obj)


class OrderedInline(admin.TabularInline):
    extra = 0
    ordering = ['order', 'id']


class SharedBackgroundAdminMixin:
    """Preview for sections that fall back to the About section's background."""

    @admin.display(description='Currently showing')
    def background_preview(self, obj):
        image = obj.background
        if not image:
            return 'No background yet - upload one here or in the About section.'
        note = '' if obj.background_image else 'Using the About section background.<br>'
        return format_html(
            '{}<img src="{}" style="max-height:120px;max-width:100%;border-radius:6px;border:1px solid #ddd">',
            mark_safe(note), image.url,
        )
