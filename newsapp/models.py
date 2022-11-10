from django.contrib.auth.models import AbstractUser
from django.db import models

from newspaper_agency import settings


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now=False)
    topic = models.ForeignKey(
        to=Topic, on_delete=models.CASCADE, related_name="newspaper"
    )
    redactor = models.ManyToManyField(to=Redactor, related_name="newspaper")

    def __str__(self):
        return f"{self.topic.name} {self.title} {self.published_date}"
