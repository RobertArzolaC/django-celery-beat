from django.contrib import admin

from .models import Order, Alert


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "symbol", "quantity", "price", "created_at")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "symbol", "type", "price", "confirmed")
