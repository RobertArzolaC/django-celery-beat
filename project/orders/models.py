import uuid

from django.db import models


class TimeStampedModel(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    confirmed_date = models.DateTimeField(null=True, blank=True)
    price = models.IntegerField(blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order: {self.id}"

    class Meta:
        ordering = ["-added"]
        get_latest_by = "-added"
