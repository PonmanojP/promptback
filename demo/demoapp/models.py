from django.db import models

class DashboardChart(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='charts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class PDFFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.name