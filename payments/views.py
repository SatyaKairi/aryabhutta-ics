import imp
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from course.models import Course

@login_required
def initiate_payment(request, *args, **kwargs):
    if request.method == "GET":
        return render(request, 'payments/pay.html')
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            amount = request.POST['amount']
            course_id = request.POST['course_id']
            # print('course id: ' + str(course_id))
            if course_id:
                course = Course.objects.get(id=course_id)
            
            installment = request.POST['installment']
        else:
            # prev_url = request.META.get('HTTP_REFERER')
            # return redirect(prev_url)
            return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

        transaction = Transaction.objects.create(made_by=user, amount=amount, course =course, installment = installment)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.username)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        # print(paytm_params)
        return render(request, 'payments/redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            print(paytm_params)
            order_id = paytm_params['ORDERID']
            print('order id '+ str(order_id))
            order_status = paytm_params['STATUS']
            transaction = Transaction.objects.get(order_id = order_id)
            received_data['COURSE']= transaction.course
            print('course is ' + str(transaction.course))
            transaction.status = order_status
            transaction.save()
        else:
            received_data['message'] = "Checksum Mismatched"
            # return render(request, 'payments/callback.html', context=received_data)

        print(received_data)
        
        return render(request, 'payments/callback.html', context=received_data)