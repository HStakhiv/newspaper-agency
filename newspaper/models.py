from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=False, default=0)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"
        ordering = ["-years_of_experience"]

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("newspaper:redactor-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now=False)
    topic = models.ForeignKey(
        to=Topic, on_delete=models.CASCADE, related_name="newspaper"
    )
    redactor = models.ManyToManyField(to=Redactor, related_name="newspaper")

    class Meta:
        ordering = ["-published_date"]

    def __str__(self) -> str:
        return f"{self.topic.name} {self.title} {self.published_date}"
