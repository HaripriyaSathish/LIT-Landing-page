from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse

from core.emails import send_site_mail
from core.models import SiteSettings

from .mixins import SingletonAdmin, image_preview


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'cloudinary_api_secret': forms.PasswordInput(render_value=True),
            'smtp_password': forms.PasswordInput(render_value=True),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    form = SiteSettingsForm
    readonly_fields = ['favicon_preview', 'og_image_preview', 'cloudinary_status', 'smtp_status', 'updated_at']
    favicon_preview = image_preview('favicon', height=48)
    og_image_preview = image_preview('og_image', height=120)

    fieldsets = [
        ('General', {
            'fields': ['site_title', 'meta_description', 'favicon', 'favicon_preview'],
            'description': 'If no favicon is uploaded, the navbar logo is used.',
        }),
        ('Main links', {
            'fields': ['join_form_url', 'booking_url'],
        }),
        ('Social sharing & analytics', {
            'fields': ['og_image', 'og_image_preview', 'google_analytics_id'],
        }),
        ('Email notifications', {
            'fields': ['notification_email'],
            'description': 'Where website enquiries are delivered.',
        }),
        ('Cloudinary (image hosting)', {
            'fields': [
                'cloudinary_status', 'use_cloudinary',
                'cloudinary_cloud_name', 'cloudinary_api_key', 'cloudinary_api_secret',
            ],
            'description': 'Find these on your Cloudinary dashboard. Save this page before uploading images elsewhere.',
        }),
        ('Email server (SMTP)', {
            'fields': [
                'smtp_status', 'smtp_host', 'smtp_port', 'smtp_username', 'smtp_password',
                'smtp_use_tls', 'smtp_use_ssl', 'from_email', 'from_name',
            ],
            'description': 'Used to send emails from the website. '
                           'After saving, click "Send test email" at the top right to check it works.',
        }),
        (None, {'fields': ['updated_at']}),
    ]

    @admin.display(description='Status')
    def cloudinary_status(self, obj):
        return '✅ Connected details saved' if obj.cloudinary_is_ready else '⚠️ Not set up - images are saved on this server'

    @admin.display(description='Status')
    def smtp_status(self, obj):
        return '✅ Details saved' if obj.smtp_is_ready else '⚠️ Not set up - emails cannot be sent'

    def get_urls(self):
        custom = [
            path(
                'send-test-email/',
                self.admin_site.admin_view(self.send_test_email),
                name='core_sitesettings_send_test_email',
            ),
        ]
        return custom + super().get_urls()

    def send_test_email(self, request):
        site = SiteSettings.load()
        change_url = reverse('admin:core_sitesettings_change', args=[site.pk])
        if not site.smtp_is_ready:
            messages.error(request, 'Please fill in and save the SMTP details first.')
            return redirect(change_url)

        recipient = site.notification_email or request.user.email or site.from_email or site.smtp_username
        try:
            send_site_mail(
                subject='Test email from your LIT website',
                message='Your website email settings are working correctly.',
                recipient_list=[recipient],
            )
        except Exception as exc:
            messages.error(request, f'Test email failed: {exc}')
        else:
            messages.success(request, f'Test email sent to {recipient}. Please check the inbox (and spam folder).')
        return redirect(change_url)
