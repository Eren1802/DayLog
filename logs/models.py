from django.db import models
from django.contrib.auth.models import User

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    done = models.TextField()
    pending = models.TextField(blank=True)
    mood = models.CharField(max_length=50, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class PendingTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = models.ForeignKey(DailyLog, on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.task[:30]}"