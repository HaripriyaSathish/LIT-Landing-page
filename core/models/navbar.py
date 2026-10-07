from django.db import models

from .base import JOIN_FORM_HELP, OrderedItem, SingletonModel, image_field, resolve_link


class Navbar(SingletonModel):
    logo = image_field('navbar', 'Logo', 'Round logo shown at the top left. PNG with transparent background works best.')
    logo_alt_text = models.CharField(
        'Logo description', max_length=150, default='London Indian Tamils (LIT) logo',
        help_text='Read out by screen readers and used by Google.',
    )
    brand_name = models.CharField('Organisation name', max_length=100, default='London Indian Tamils')
    brand_highlight = models.CharField(
        'Highlighted name', max_length=50, blank=True, default='(LIT)',
        help_text='Shown in the accent colour next to the organisation name.',
    )
    tagline = models.CharField('Tagline', max_length=150, blank=True, default='CONNECT • SUPPORT • CELEBRATE')
    sub_tagline = models.CharField(
        'Small text under tagline', max_length=200, blank=True,
        default='India in our heart. London in our home. Tamil in our identity.',
    )
    show_button = models.BooleanField('Show button', default=True)
    button_text = models.CharField('Button text', max_length=50, default='JOIN LIT')
    button_link = models.CharField('Button link', max_length=500, blank=True, help_text=JOIN_FORM_HELP)

    class Meta:
        verbose_name = 'Navbar'
        verbose_name_plural = 'Navbar'

    def __str__(self):
        return 'Navbar'

    @property
    def button(self):
        url, new_tab = resolve_link(self.button_link)
        return {'text': self.button_text, 'url': url, 'new_tab': new_tab}

    @property
    def active_links(self):
        return self.links.filter(is_active=True)


class NavLink(OrderedItem):
    navbar = models.ForeignKey(Navbar, on_delete=models.CASCADE, related_name='links')
    label = models.CharField('Menu text', max_length=50)
    link = models.CharField(
        'Link', max_length=255,
        help_text='Use #section-name to scroll to a section (e.g. #about), or a full web address.',
    )
    open_in_new_tab = models.BooleanField('Open in new tab', default=False)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Menu link'
        verbose_name_plural = 'Menu links'

    def __str__(self):
        return self.label
