from django.shortcuts import render, get_object_or_404
from orders.models import Order
from .tasks import payment_completed


from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from .config import MERCHANT


client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000
descrtption = ""
mobile = "09123431503"
CallbackURL = 'http://localhost:8000/zarinpal/verify/'


def send_request(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    result = client.service.PaymentRequest(MERCHANT, total_cost, descrtption, order.email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay')
    else:
        return HttpResponse('Error code: ' + str(result.Status))
    

def verify(request):
    if request.GET.get('Status') == 'OK':
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            order.paid = True
            order.save()
            payment_completed.delay(order.id)
            return render(request, "zarinpal/success.html", {"id":result.RefID}) 
        elif result.Status == 101:
            # return HttpResponse('Transaction submited\n' + str(result.Status))
            return render('zarinpal/submited.html',{'status':result.Status})
        else:
            # return HttpResponse('Transaction faild\nStatus: ' + str(result.Status))
            return render('zarinpal/faild.html', {'status':result.Status})
    else:
        # return HttpResponse('Transaction faild or canseld by user')
        return render('zarinpal/cansel.html')