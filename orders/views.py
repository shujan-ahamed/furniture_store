from django.shortcuts import render, redirect, HttpResponse
from accounts.models import User
from accounts.utils import send_notification
from marketplace.models import Products, Tax

from orders.models import Coupon, Order, OrderProduct, Payment
from .forms import CouponApplyForm, OrderForm

from django.http import JsonResponse
from django.utils import timezone

from django.contrib.sites.shortcuts import get_current_site

import datetime
import json

# Create your views here.
def place_order(request):
    sub_total = 0
    grand_total = 0
    total_tax = 0
    discount = 0
    shipping_cost = 0
    coupon = None
    tax =0
    get_tax = Tax.objects.filter(is_active = True)

    #get shipping cost from session 
    if 'shipping_cost' in request.session:
        shipping_cost = request.session['shipping_cost']
        print(shipping_cost)
    else:
        shipping_cost = 0
    if 'shipping_method' in request.session:
        shipping_method = request.session['shipping_method']
        print(shipping_method)
    else:
        shipping_method = None

    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            sub_total += int(item['price']) * float(item['qty'])

    try:
        coupon_id  = request.session['coupon_id']
        if coupon_id:
            coupon = Coupon.objects.get(id= coupon_id)
            discount = (coupon.discount / 100) * sub_total
    except:
        discount = 0

    dis_sub_total = sub_total- discount
    # CALCULATE  Tax
    tax_dict = {}
    for i in get_tax:
        tax_type = i.tax_type
        percentage = float(i.tax_percentage)
        tax = round(dis_sub_total* percentage/100, 2)
        tax_dict.update({tax_type:{str(percentage):tax}})

    for key,val in tax_dict.items():
        for i,j in val.items():
            total_tax +=j
    
    grand_total = dis_sub_total + total_tax + shipping_cost

    if request.method == 'POST':
        
        print('posting')
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pin_code = form.cleaned_data['pin_code']
            data.order_note = form.cleaned_data['order_note']
            data.tax_data = json.dumps(tax_dict)
            data.total_tax = total_tax
            data.coupon = coupon
            data.discount = discount
            data.shipping_method = shipping_method
            data.shipping_cost = shipping_cost
            data.order_subtotal = sub_total
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            print(data.pin_code)
            print('done')

            context = {
                'cart_data':request.session['cartdata'],
                'sub_total': sub_total,
                'total_cart_items':len(request.session['cartdata']),
                "tax" : tax,
                "tax_dict" : tax_dict,
                'total_tax': total_tax,
                'grand_total' : grand_total,
                'order':data,
                'dis_sub_total' : dis_sub_total,
            }
            return render(request, 'order/place_order.html', context)
        else:
            print(form.errors)
            print('err')

    # order = Order.objects.get(user = current_user, is_ordered=False, order_number= order_number)
    context = {
        'cart_data':request.session['cartdata'],
        'sub_total': sub_total,
        'total_cart_items':len(request.session['cartdata']),
        "tax" : tax,
        "tax_dict" : tax_dict,
        'total_tax': total_tax,
        'grand_total' : grand_total,
    }
    return render(request, 'order/place_order.html',context)


def confirm_order(request):
    return render(request, "order/confirm_order.html")


def payment(request):
    # Check if the request is ajax or not
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
    # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
            transaction_id = request.POST.get('transaction_id')
            order_number = request.POST.get('order_number')
            payment_method = request.POST.get('payment_method')
            status = request.POST.get('status')

            order = Order.objects.get(user = request.user, order_number = order_number)
            payment = Payment(
                user = request.user,
                payment_id =transaction_id,
                payment_method = payment_method,
                status = status,
                ammount_paid = order.order_total
            )
            payment.save()
    # UPDATE THE ORDER MODEL
            order.is_ordered = True
            order.status = 'paid'
            order.payment = payment
            order.save()
    # MOVE THE CART ITEMS TO ORDERED FOOD MODEL
            
            if 'cartdata' in request.session:
                cart_items = request.session['cartdata'].items()
                print(cart_items)
                for p_id,item in cart_items:
                    print(type(p_id))
                    ordered_product = OrderProduct()
                    ordered_product.order = order
                    ordered_product.payment = payment
                    ordered_product.invoice_numr = transaction_id
                    ordered_product.user = request.user
                    ordered_product.product = Products.objects.get(pk=int(item['id']), is_available = True)
                    ordered_product.quantity = item['qty']
                    ordered_product.product_price = item['price']
                    ordered_product.total_amount = int(item['price']) * float(item['qty']) # total amount

                    ordered_product.product_size = item['product_size']
                    ordered_product.product_colour = item['product_colour']
                    ordered_product.product_image_url = item['image']
                    ordered_product.save()

    # SEND ORDER CONFIRMATION EMAIL TO THE CUSTOMER
            #send info notification
            mail_subject = "Thank you sir, for your order."
            mail_template = 'mail/order_notification.html'

            ordered_product = OrderProduct.objects.filter(order=order)

            sub_total = 0
            for  item in ordered_product:
                sub_total += item.total_amount

            tax_data = json.loads(order.tax_data)
            context= {
                'user' : request.user,
                'order' : order,
                'to_email' : order.email,
                'ordered_product' : ordered_product,
                'domain' : get_current_site(request),
                'subtotal' : sub_total,
                'order_total' : order.order_total,
                'tax' : order.total_tax,
                'tax_data' : tax_data,
            }
            send_notification(mail_subject, mail_template, context)
            print('email, done')
            
    # SEND ORDER RECEIVED EMAIL TO THE VENDOR
            admin_info = User.objects.get(is_superadmin= True)
            admin_email = admin_info.email
            mail_subject = "Congrats, you have recived a new order."
            mail_template = 'mail/order_recieved_notification.html'

            context= {
                'user' : request.user,
                'order' : order,
                'to_email' : admin_email,
                'ordered_product' : ordered_product,
                'sub_total' : sub_total,
                'order_total' : order.order_total,
                'tax' : order.total_tax,
                'tax_data' : tax_data,
            }
            send_notification(mail_subject, mail_template, context)
            print('email, done vendor')

    # CLEAR THE CART IF THE PAYMENT IS SUCCESS
            if 'cartdata' in request.session:
                del request.session['cartdata']

    # CLEAR THE Coupon IF THE PAYMENT IS SUCCESS
            if 'coupon_id' in request.session:
                del request.session['coupon_id']

    #SEND BACKAJAX REQUEST WITH SUCCESS OR FAILIURE
            response = {
                'order_number' : order_number,
                'transaction_id' : transaction_id,
            }
            return JsonResponse(response)
        

def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('transaction_id')
    dis_sub_total = 0
    
    order = Order.objects.get(order_number = order_number, is_ordered = True, payment__payment_id  = transaction_id)
    ordered_products = OrderProduct.objects.filter(order = order)

    sub_total = 0
    for item in ordered_products:
        sub_total += (item.product_price * item.quantity)
    
    dis_sub_total = order.order_subtotal - order.discount
    tax_data = json.loads(order.tax_data)
    context = {
        'order' : order,
        'ordered_products' : ordered_products,
        'sub_total' : sub_total,
        'tax_data' : tax_data,
        'dis_sub_total' : dis_sub_total,
    }
    return render(request, 'order/order_complete.html', context)

def order_details(request, order_number):
    order = Order.objects.get(user= request.user, order_number = order_number, is_ordered = True)
    ordered_products = OrderProduct.objects.filter(order = order)

    sub_total = 0
    for item in ordered_products:
        sub_total += (item.product_price * item.quantity)
    
    
    tax_data = json.loads(order.tax_data)
    contex = {
        'order' : order,
        'ordered_products' : ordered_products,
        'sub_total' : sub_total,
        'tax_data' : tax_data,
    }
    return render(request, 'order/order_details.html', contex)

#cuppon apply
def coupon_apply(request):
    now = timezone.now()
    print(now)
    form = CouponApplyForm(request.POST)
    print('ok')
    if form.is_valid():
        code = form.cleaned_data['code']
        print('done')
        try:
            coupon = Coupon.objects.get(code__iexact = code, valid_from__lte = now, valid_to__gte =now, active =True)
            request.session['coupon_id'] = coupon.id
            print('ok done')
            print(request.session['coupon_id'])
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = code
    else:
        form.errors
        print('err')
    return redirect('checkout')

