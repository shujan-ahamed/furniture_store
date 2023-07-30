from django.shortcuts import render, redirect
from carts.models import Cart, CartItem, Tax
from django.http import JsonResponse
from marketplace.models import ProductVariation, Products

from django.template.loader import render_to_string

def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart

# Create your views here.
def add_cart(request, product_id):
    variation = ProductVariation.objects.get(product_id = request.GET['id'], size__title = request.GET['product_size'], colour__title = request.GET['product_colour']) 
    
    cart_p = {}
    cart_p[variation.id] = {
        'id' : request.GET['id'],
        'var_id' : variation.id,
        'image' : request.GET['image'],
        'product_url' : request.GET['product_url'],
        'product_size' : request.GET['product_size'],
        'product_colour' : request.GET['product_colour'],
        'title' : request.GET['title'],
        'qty' : int(request.GET['qty']),
        'or_price' : request.GET['or_price'],
        'price' : request.GET['price'],
    }
    #check if any cart exist in the session

    print(request.session)

    if 'cartdata' in request.session:
        #check if certain product exist in the same cart
        if str(variation.id) in request.session['cartdata']:
            #check if the variation are same
            cart_item= request.session['cartdata']
            cart_item[str(variation.id)]['qty']+=int(request.GET['qty'])
            cart_item.update(cart_item)
            request.session['cartdata']= cart_item

            total = 0
            for p_id,item in request.session['cartdata'].items():
                total += int(item['price']) * float(item['qty'])
            
            return JsonResponse({'data':request.session['cartdata'], 'total_cart_items':len(request.session['cartdata']), 'status': 'success','message': 'Cart item added.', 'total':total})
            
        else:
            cart_item= request.session['cartdata']
            cart_item.update(cart_p)
            request.session['cartdata']= cart_item
            total = 0
            for p_id,item in request.session['cartdata'].items():
                total += int(item['price']) * float(item['qty'])
                
            return JsonResponse({'data':request.session['cartdata'], 'total_cart_items':len(request.session['cartdata']), 'status': 'success','message': 'Cart item added.', 'total':total})
    else:
        request.session['cartdata'] = cart_p
        return JsonResponse({'data':request.session['cartdata'], 'total_cart_items':len(request.session['cartdata']), 'status': 'success','message': 'Cart item added.', 'total':total})

def decrease_cart(request):
    
    product_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if product_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            if cart_data[str(request.GET['id'])]['qty'] >1:
                cart_data[str(request.GET['id'])]['qty']-=1
                cart_data.update(cart_data)
                request.session['cartdata'] = cart_data

                total = 0
                for p_id,item in request.session['cartdata'].items():
                    total += int(item['price']) * float(item['qty'])
                    
                t = render_to_string('ajax/cart_list.html',{'cart_data':request.session['cartdata'], 'total':total, 'total_cart_items':len(request.session['cartdata'])})
                return JsonResponse({'data':t, 'total_cart_items':len(request.session['cartdata'])})
            else:
                cart_data = request.session['cartdata']
                del request.session['cartdata'][product_id]
                request.session['cartdata'] = cart_data
                total = 0
                for p_id,item in request.session['cartdata'].items():
                    total += int(item['price']) * float(item['qty'])
                    
                t = render_to_string('ajax/cart_list.html',{'cart_data':request.session['cartdata'], 'total':total, 'total_cart_items':len(request.session['cartdata'])})
                return JsonResponse({'data':t, 'total_cart_items':len(request.session['cartdata']), 'status': 'success','message': 'Cart item deleted.'})

def increase_cart(request):
    product_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if product_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']+=1
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
    total = 0
    for p_id,item in request.session['cartdata'].items():
        total += int(item['price']) * float(item['qty'])
        
    t = render_to_string('ajax/cart_list.html',{'cart_data':request.session['cartdata'], 'total':total, 'total_cart_items':len(request.session['cartdata'])})
    return JsonResponse({'data':t, 'total_cart_items':len(request.session['cartdata'])})

def remove_cart(request):
    product_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if product_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][product_id]
            request.session['cartdata'] = cart_data

            total = 0
            for p_id,item in request.session['cartdata'].items():
                total += int(item['price']) * float(item['qty'])
                
            t = render_to_string('ajax/cart_list.html',{'cart_data':request.session['cartdata'], 'total':total, 'total_cart_items':len(request.session['cartdata'])})
            return JsonResponse({'data':t, 'total_cart_items':len(request.session['cartdata']), 'status': 'success','message': 'Cart item deleted.'})
            
        else:
            total = 0
            for p_id,item in request.session['cartdata'].items():
                total += int(item['price']) * float(item['qty'])
                
            t = render_to_string('ajax/cart_list.html',{'cart_data':request.session['cartdata'], 'total':total, 'total_cart_items':len(request.session['cartdata'])})
            return JsonResponse({'data':t, 'total_cart_items':len(request.session['cartdata']), 'status': 'error','message': "Product doesn't exist in cart list."})

    

def cart(request, total = 0,tax = 0, quantity = 0, item_total = 0, total_tax=0, grand_total=0):
    
    for p_id,item in request.session['cartdata'].items():

        
        print((float(item['qty'])))
        
        

    context = {
        'quantity' : quantity,
        'total' : total,
        'tax' : tax,
        'total_tax' : total_tax,
        'grand_total' : grand_total,
    }
    return render(request, "marketplace/cart.html",{'cart_data':request.session['cartdata'], 'total':total, 'total_cart_items':len(request.session['cartdata'])})