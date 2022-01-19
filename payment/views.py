from django.shortcuts import render
from dotenv import load_dotenv, find_dotenv
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
import json
import os
from django.shortcuts import redirect


load_dotenv(find_dotenv())

key_id = os.environ['key_id']
key_secret = os.environ['key_secret']

razorpay_client = razorpay.Client(auth=(key_id, key_secret))

amount = 0

def newamount(price):
    global amount
    amount = price

def homepage(request):
    return render(request, 'index.html')

def successpage(request):
    return render(request, 'success.html')
 
@csrf_exempt
def updateamount(request):
    currency = 'INR'
    amount = request.GET.get('amount')  # Rs. 200 

    newamount(amount)
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']

    if amount == '27000':
        callback_url = 'paymenthandler270/'
    else:
        callback_url = 'paymenthandler360/'

    # we need to pass these details to frontend.
    context = {}
    context['type'] = "paymentupdated"
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = key_id
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return HttpResponse(json.dumps(context), content_type="application/json")

from django.core.mail import EmailMessage
from django.conf import settings

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler270(request):
    if request.method == "GET":
        return homepage(request)
    # only accept POST request.
    if request.method == "POST":
        amount = '27000'
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')

            razorpay_order_id = request.POST.get('razorpay_order_id', '')

            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            context = {}
            context["type"] = "success"
            context["payment_id"] = payment_id
            context["order_id"] = razorpay_order_id
            context["signature"] = signature

            if result is None:
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    return render(request, 'success.html', context) 
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

@csrf_exempt
def paymenthandler360(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            amount = '36000'
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')

            razorpay_order_id = request.POST.get('razorpay_order_id', '')

            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            context = {}
            context["type"] = "success"
            context["payment_id"] = payment_id
            context["order_id"] = razorpay_order_id
            context["signature"] = signature

            if result is None:
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    return render(request, 'success.html', context) 
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
