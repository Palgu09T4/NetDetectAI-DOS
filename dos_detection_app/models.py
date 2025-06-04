from django.db import models
from django.contrib.auth.models import User

class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='uploads/')   # Uploaded CSV
    output_file = models.FileField(upload_to='outputs/', null=True, blank=True)  # Prediction result CSV
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255)
    dos_count = models.IntegerField(default=0)
    normal_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.original_filename} by {self.user.username} on {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
