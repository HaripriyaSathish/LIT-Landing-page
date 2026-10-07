from django.db import models

FOUNDER_BIO = (
    "London Indian Tamils was founded by Sathish Duraisamy with a simple vision - to create a stronger, "
    "more connected and supportive community for Tamil-speaking Indians living across the UK.\n\n"
    "Having lived in the UK for many years and been actively involved in community, cultural and social "
    "initiatives, Sathish wanted to create a platform that goes beyond events and WhatsApp conversations - "
    "a community where people can build friendships, support careers and businesses, share opportunities "
    "and celebrate Tamil culture together.\n\n"
    "His vision for LIT is to bring people together across generations, professions and locations, creating "
    "meaningful connections and a community that supports one another."
)
FOUNDER_QUOTE = 'LIT is about people, relationships and creating something valuable for the community - together.'

from core.icons import ICON_CHOICES

from .base import OrderedItem, SingletonModel, image_field


class AboutSection(SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    section_label = models.CharField('Small label above heading', max_length=50, blank=True, default='ABOUT LIT')
    heading = models.CharField('Heading', max_length=200, default='More Than a WhatsApp Group.')
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=200, blank=True, default='A Community.',
        help_text='Shown in the accent colour (italic) after the heading.',
    )
    paragraph_1 = models.TextField('First paragraph', blank=True)
    paragraph_2 = models.TextField('Second paragraph', blank=True)

    background_image = image_field(
        'about', 'Section background image', 'The patterned background behind the whole section.',
    )

    image = image_field('about', 'Photo', 'Portrait photo shown on the left, about 800x1000 px.')
    image_alt_text = models.CharField('Photo description', max_length=200, blank=True)
    badge_title = models.CharField(
        'Photo badge - big text', max_length=50, blank=True, default='தமிழ்',
        help_text='The small card on the corner of the photo. Leave empty to hide it.',
    )
    badge_subtitle = models.CharField('Photo badge - small text', max_length=50, blank=True, default='ONE COMMUNITY')

    # Founder
    show_founder = models.BooleanField('Show founder block', default=True)
    founder_name = models.CharField('Founder name', max_length=100, blank=True, default='Sathish Duraisamy')
    founder_role = models.CharField(
        'Founder title', max_length=150, blank=True, default='Founder & Director, London Indian Tamils',
    )
    founder_bio = models.TextField(
        'Founder introduction', blank=True, default=FOUNDER_BIO,
        help_text='Leave a blank line between paragraphs. Keep it short - the personal website carries the full story.',
    )
    founder_quote = models.CharField(
        'Founder quote', max_length=300, blank=True, default=FOUNDER_QUOTE,
        help_text='Quotation marks are added automatically.',
    )
    founder_button_text = models.CharField('Button text', max_length=50, blank=True, default='ABOUT SATHISH')
    founder_button_link = models.URLField(
        'Button link', max_length=500, blank=True,
        help_text="Sathish's personal website Founder/About page (opens in a new tab). "
                  "While empty, the button scrolls to the Contact section.",
    )

    class Meta:
        verbose_name = 'About Section'
        verbose_name_plural = 'About Section'

    def __str__(self):
        return 'About Section'

    @property
    def founder_paragraphs(self):
        return [p.strip() for p in self.founder_bio.replace('\r\n', '\n').split('\n\n') if p.strip()]

    @property
    def active_pillars(self):
        return self.pillars.filter(is_active=True)


class AboutPillar(OrderedItem):
    about = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='pillars')
    icon = models.CharField('Icon', max_length=50, choices=ICON_CHOICES, default='users')
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description', blank=True)
    is_highlighted = models.BooleanField(
        'Highlight', default=False,
        help_text='Keeps the gold border and gold title on all the time (normally they only show on hover).',
    )

    class Meta(OrderedItem.Meta):
        verbose_name = 'Card'
        verbose_name_plural = 'Cards (Connect / Support / Celebrate) - numbers 01, 02, 03 are added automatically'

    def __str__(self):
        return self.title
