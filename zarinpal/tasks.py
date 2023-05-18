from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"My Shop - order no {order_id}"
    message = "please check Aatached invoice"
    email = EmailMessage(subject, message, 'admin@admin.com', [order.email])
    html = render_to_string("orders/order/pdf.html", {"order" : order})
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT+'css/pdf.css')]
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out, stylesheets)
    email.attach(f'order_{order.id}', out.getvalue(), 'application/pdf')
    email.send()