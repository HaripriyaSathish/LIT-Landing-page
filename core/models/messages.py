from django.db import models

from .base import OrderedItem, SharedBackgroundMixin, SingletonModel, image_field


class MessagesSection(SharedBackgroundMixin, SingletonModel):
    is_active = models.BooleanField('Show this section', default=True)
    background_image = image_field(
        'messages', 'Section background image', SharedBackgroundMixin.SHARED_BACKGROUND_HELP,
    )
    section_label = models.CharField(
        'Small label above heading', max_length=50, blank=True, default='VOICES OF SUPPORT',
    )
    heading = models.CharField('Heading', max_length=200, default='Messages to the')
    heading_highlight = models.CharField(
        'Highlighted heading', max_length=200, blank=True, default='LIT Community',
        help_text='Shown in the accent colour (italic) after the heading.',
    )
    description = models.TextField('Description', blank=True)

    follow_text_before = models.CharField('Follow line - text before', max_length=100, blank=True, default='Follow')
    follow_handle = models.CharField(
        'Follow line - Instagram name', max_length=100, blank=True, default='@londonindiantamils',
        help_text='Shown in gold and links to Instagram. Leave all three parts empty to hide the line.',
    )
    follow_text_after = models.CharField(
        'Follow line - text after', max_length=200, blank=True,
        default='for more community stories, messages and updates.',
    )
    follow_link = models.URLField(
        'Instagram link', max_length=500, blank=True,
        default='https://www.instagram.com/londonindiantamils/',
    )

    class Meta:
        verbose_name = 'Messages Section'
        verbose_name_plural = 'Messages Section'

    def __str__(self):
        return 'Messages Section'

    @property
    def active_messages(self):
        return self.messages.filter(is_active=True)


class SupportMessage(OrderedItem):
    section = models.ForeignKey(MessagesSection, on_delete=models.CASCADE, related_name='messages')
    photo = image_field('messages', 'Photo', 'Portrait photo, about 600x800 px.')
    name = models.CharField('Name', max_length=100)
    role = models.CharField('Role / title', max_length=100, blank=True)
    status_text = models.CharField(
        'Status text', max_length=100, blank=True, default='',
        help_text='Optional small gold text under the role.',
    )
    button_text = models.CharField('Button text', max_length=50, blank=True, default='Watch Message')
    video_link = models.URLField(
        'Video link', max_length=500, blank=True,
        help_text='YouTube, Instagram or Cloudinary video link. The photo and the button both open it. '
                  'Leave empty and they open the Instagram page.',
    )

    class Meta(OrderedItem.Meta):
        verbose_name = 'Message card'
        verbose_name_plural = 'Message cards'

    def __str__(self):
        return self.name

    @property
    def has_video(self):
        return bool(self.video_link)

    @property
    def button_url(self):
        return self.video_link or self.section.follow_link
