from django.db import models
from django.urls import reverse
from hongstagram import settings

class Post(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, verbose_name='작성자')
    text = models.TextField(max_length=1000)

    def __str__(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])
    
    class Meta:
        db_table = "포스트"
        verbose_name = "포스트"

