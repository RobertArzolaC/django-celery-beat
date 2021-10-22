import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER

from .models import Alert


logger = get_task_logger(__name__)


@shared_task
def send_message(current_price, operation):
    operation = "venta" if operation == "sell" else "compra"
    send_mail(
        "🚨🤩 Bot Trading 🤩🚨",
        f" El precio actual es de {current_price} dólares. Llego la hora de abrir una operación de {operation}.",
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
        alerts_unconfirmed = Alert.objects.filter(confirmed=False)
        if alerts_unconfirmed:
            logger.info(f"Current price: {current_price}")
            last_alert = alerts_unconfirmed.latest()
            if (
                last_alert.type == Alert.TAKE_PROFIT
                and float(current_price) > last_alert.price
            ):
                last_alert.confirmed = True
                last_alert.save()
                send_message.apply_async([current_price, "sell"])
            elif (
                last_alert.type == Alert.STOP_LOSS
                and float(current_price) < last_alert.price
            ):
                last_alert.confirmed = True
                last_alert.save()
                send_message.apply_async([current_price, "buy"])
        else:
            logger.info("No scheduled alerts found ...")
