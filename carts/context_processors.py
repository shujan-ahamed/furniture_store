from carts.views import _cart_id
from .models import Cart, CartItem


def counter(request, cart=None, cart_items=None):
    count = 0
    try:
        cart = Cart.objects.filter(cart_id = _cart_id(request))
        cart_items = CartItem.objects.all().filter(cart = cart[:1])

        if cart_items:
            for cart_item in cart_items:
                count+= cart_item.quantity
        
    except Cart.DoesNotExist:
        count = 0
    
    return dict(count = count)