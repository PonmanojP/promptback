from django.db import models
from django.contrib.auth.models import User

class DashboardChart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='charts')  # Associate with User
    description = models.TextField()
    image = models.ImageField(upload_to='charts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class PDFFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdf_files')  # Associate with User
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.name
