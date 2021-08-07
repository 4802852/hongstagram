from django.db import models
from django.urls import reverse
from hongstagram import settings

import uuid, re
from datetime import datetime
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, Resize, ResizeToFit


class Hashtag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


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
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_post", blank=True)

    def hashtag_save(self):
        self.hashtags.set([])
        hashtagset = re.findall(r"#(\w+)\b", self.text)

        if not hashtagset:
            return

        for tag in hashtagset:
            tag, tag_created = Hashtag.objects.get_or_create(name=tag)
            self.hashtags.add(tag)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("post-detail", args=[str(self.id)])

    class Meta:
        db_table = "Post"
        verbose_name = "Post"


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image = ProcessedImageField(
        upload_to=get_file_path,
        processors=[ResizeToFill(width=700, height=700, upscale=True)],
        null=True,
        blank=True,
        format="JPEG",
        options={"quality": 90},
    )


class Comment(models.Model):
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="작성자",
    )
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.id
