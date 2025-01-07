from django.db import models

# Create your models here.

class TechExample(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technology_used = models.CharField(max_length=200)
    link = models.URLField(blank=True)
    image = models.ImageField(upload_to='tech_images/', blank=True)

    def __str__(self):
        return self.title


class WritingExample(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateField()
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title
