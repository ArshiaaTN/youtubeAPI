from django.db import models
from videos.models import Video
from subscriptions.models import Subscription

class VideoSubscription(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    quality = models.CharField(max_length=10, choices=[('480p', '480p'), ('720p', '720p'), ('1080p', '1080p')])

    def __str__(self):
        return f"Video {self.video.title} in {self.subscription.type} with {self.quality} quality"
