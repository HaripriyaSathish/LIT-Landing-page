from django.core.mail import EmailMultiAlternatives

from core.models import SiteSettings


def send_site_mail(subject, message, recipient_list=None, html_message=None, reply_to=None):
    """Send an email using the SMTP details from Site Settings.

    If recipient_list is empty, it goes to the notification email in Site Settings.
    """
    site = SiteSettings.load()
    recipients = recipient_list or [site.notification_email]
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=site.formatted_from_email,
        to=recipients,
        reply_to=reply_to,
    )
    if html_message:
        email.attach_alternative(html_message, 'text/html')
    return email.send()
