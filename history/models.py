from django.db import models
from accounts.models import User
from videos.models import Video

class History(models.Model):
    watch_date = models.DateField()
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} watched {self.video.title} on {self.watch_date}"
