from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField

from pages.blocks import BaseStreamBlock


class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'projects.ProjectPage', on_delete=models.CASCADE, related_name='tagged_items')


class ProjectIndexPage(Page):
    intro = models.CharField(max_length=1000, blank=True)
    icon = models.CharField(max_length=20, blank=True)

    api_fields = [
        APIField('intro'),
        APIField('icon'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('icon'),

    ]

    subpage_types = [
        'projects.ProjectPage',
    ]


class ProjectPage(Page):
    project_url = models.CharField(
        max_length=250, blank=True, help_text='Ex: Github url')
    demo_url = models.CharField(
        max_length=250, blank=True, help_text='Url for demo of project')
    intro = models.CharField(max_length=250, blank=True,
                             help_text='a couple sentance introduction')
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    about = models.TextField(blank=True)

    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    api_fields = [
        APIField('project_url'),
        APIField('demo_url'),
        APIField('intro'),
        APIField('body'),
        APIField('tags'),
        APIField('gallery_images')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('project_url'),
        FieldPanel('demo_url'),
        FieldPanel('intro'),
        StreamFieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel('tags'),
    ]


class ProjectPageGalleryImage(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    api_fields = [
        APIField('image'),
        APIField('caption'),
        APIField('page'),
        APIField('image_thumbnail', serializer=ImageRenditionField(
            'fill-100x100', source='image')),
        APIField('image_medium', serializer=ImageRenditionField(
            'fill-300x300', source='image')),
        APIField('image_banner', serializer=ImageRenditionField(
            'fill-500x400', source='image')),
        APIField('image_full', serializer=ImageRenditionField(
            'max-800x800', source='image'))
    ]

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class ProjectResources(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE,
                       related_name='resources')
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=200, blank=True)

    api_fields = [
        APIField('item')
    ]

    panels = [
        FieldPanel('item')
    ]
