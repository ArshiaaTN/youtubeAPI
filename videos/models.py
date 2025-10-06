from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField()
    video_url = models.URLField()

    def __str__(self):
        return self.title
