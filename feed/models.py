from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings


class Loop(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=60)
    lane = models.CharField(max_length=1, blank=True, null=True)
    link = models.CharField(max_length=400, blank=True, null=True)
    image = CloudinaryField('image', default=' ', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    class Meta:
        ordering = ['-created_at', ]