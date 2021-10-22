import uuid

from django.db import models
from django.utils.translation import gettext as _


class TimeStampedModel(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Alert(TimeStampedModel):
    STOP_LOSS = "SL"
    TAKE_PROFIT = "TP"
    ALERT_TYPE_CHOICES = [
        (STOP_LOSS, _("Stop Loss")),
        (TAKE_PROFIT, _("Take Profit")),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        _("Type"),
        max_length=2,
        choices=ALERT_TYPE_CHOICES,
        default=TAKE_PROFIT,
    )
    symbol = models.CharField(_("Symbol"), blank=True, null=True, max_length=20)
    price = models.FloatField(_("Price"), blank=True, null=True)
    confirmed = models.BooleanField(_("Confirmed"), default=False)

    def __str__(self):
        return f"Alert: {self.id}"

    class Meta:
        ordering = ["-added"]
        get_latest_by = "-added"
        verbose_name = _("Alert")
        verbose_name_plural = _("Alerts")


class Order(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    symbol = models.CharField(_("Symbol"), blank=True, null=True, max_length=20)
    binance_id = models.SmallIntegerField(_("Id Binance"), blank=True, null=True)
    price = models.FloatField(_("Price"), blank=True, null=True)
    quantity = models.FloatField(_("Quantity"), blank=True, null=True)
    type = models.CharField(_("Type"), blank=True, null=True, max_length=20)
    side = models.CharField(_("Side"), blank=True, null=True, max_length=20)
    created_at = models.DateTimeField(_("Created At"), null=True)

    def __str__(self):
        return f"Order: {self.id}"

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
