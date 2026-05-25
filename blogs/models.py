from django.db import models
from core.models import BaseModel
from django.utils.text import slugify


class PostStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"


class Blog(BaseModel):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to="blog_covers/", null=True, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=PostStatus.choices)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
