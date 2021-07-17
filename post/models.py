from django.db import models
from django.urls import reverse
from hongstagram import settings

import uuid
from datetime import datetime
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, Resize, ResizeToFit


def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime("%Y/%m/%d")
    uuid_name = uuid.uuid4().hex
    return "/".join(["upload_files/", ymd_path, uuid_name])


class Post(models.Model):
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="작성자",
    )
    text = models.TextField(max_length=1000)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])

    class Meta:
        db_table = "Post"
        verbose_name = "Post"


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image = ProcessedImageField(
        upload_to=get_file_path,
        processors=[ResizeToFit(width=500, height=500, upscale=True)],
        null=True,
        blank=True,
        format="JPEG",
        options={"quality": 90},
    )
