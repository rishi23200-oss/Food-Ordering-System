from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import OrderItem


@shared_task
def send_order_email(email, user_name, order_id, address):

    order_items = OrderItem.objects.filter(order_id=order_id)

    html_message = render_to_string(
        "emails/bill_invoice_template.html",
        {
            "user": user_name,
            "order_items": order_items,
            "address": address,
        },
    )

    plain_message = strip_tags(html_message)

    send_mail(
        "Your order & payment is successful ✅",
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html_message,
    )