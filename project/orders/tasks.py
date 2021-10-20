import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER

from .models import Order


logger = get_task_logger(__name__)


@shared_task
def send_message(current_price):
    send_mail(
        "🚨🤩 Bot Trading 🤩🚨",
        f" El precio actual es de {current_price} dólares. Llego la hora de vender.",
        EMAIL_HOST_USER,
        ["robert.arzola.c@gmail.com", "seminariohillaryllerena@gmail.com"],
        fail_silently=False,
    )


@shared_task
def get_price_btc():
    api_url = "https://api.coinbase.com/v2/prices/spot?currency=USD"
    response = requests.get(api_url)
    if response.ok:
        data = response.json()
        current_price = data["data"]["amount"]
        orders_unconfirmed = Order.objects.filter(confirmed=False)
        if orders_unconfirmed:
            last_order = orders_unconfirmed.latest()
            if float(current_price) > last_order.price:
                last_order.confirmed = True
                last_order.save()
                send_message.apply_async([current_price])
        else:
            logger.info("Not found orders saved ...")
